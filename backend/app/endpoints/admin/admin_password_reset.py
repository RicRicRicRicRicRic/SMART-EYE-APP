# app/endpoints/admin/admin_password_reset.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List
import secrets
import string
import logging
import os
import smtplib
from email.mime.text import MIMEText

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder
from ...models.password_reset import PasswordResetRequest as ResetModel
from ...schemas.admin.admin import (
    PasswordResetRequest, 
    PasswordResetResponse
)

router = APIRouter(prefix="/admin", tags=["Admin Password Reset"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  

def generate_random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for i in range(length))

@router.get("/password-reset/requests", response_model=List[dict])
async def get_password_reset_requests(db: Session = Depends(get_db)):
    """Core Point of Failure Fix: Fetch and list pending password reset submissions"""
    try:
        requests = db.query(
            ResetModel,
            EmergencyResponder.full_name,
            EmergencyResponder.email
        ).join(
            EmergencyResponder, 
            ResetModel.responder_id == EmergencyResponder.responder_id
        ).all()
        
        result = []
        for req, name, email in requests:
            result.append({
                "request_id": getattr(req, "request_id", None),
                "responder_id": req.responder_id,
                "full_name": name,
                "email": email,
                "status": getattr(req, "status", "pending"),
                "created_at": getattr(req, "created_at", None)
            })
        return result
    except Exception as e:
        logging.error(f"Failed to query database password reset tickets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve password reset entries"
        )

@router.post("/password-reset", response_model=PasswordResetResponse)
async def reset_responder_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Reset password for a specific email and send it directly via Email"""
    try:
        responder = db.query(EmergencyResponder).filter(
            EmergencyResponder.email == request.email.strip().lower()
        ).first()

        if not responder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist"
            )

        new_password = generate_random_password(12)
        hashed_password = pwd_context.hash(new_password)

        responder.hashed_password = hashed_password
        db.commit()
        db.refresh(responder)

        logging.info(f"Password reset for: {request.email}")

        try:
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            sender_email = os.getenv("SMTP_EMAIL")
            sender_password = os.getenv("SMTP_PASSWORD")

            if not all([sender_email, sender_password]):
                raise Exception("Missing SMTP credentials in environmental layout context")

            message_body = f"""
Dear {responder.full_name or 'Emergency Responder'},

Your SMART-EYE account password has been successfully reset.

New Password: {new_password}

Please log in and update your password immediately within your account dashboard settings.
"""
            msg = MIMEText(message_body.strip())
            msg["Subject"] = "SMART-EYE Administrative Password Reset"
            msg["From"] = sender_email
            msg["To"] = responder.email

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [responder.email], msg.as_string())
            server.quit()
            
            logging.info(f"Notification email dispatched cleanly to {responder.email}")

        except Exception as email_error:
            logging.error(f"Email delivery gateway crash: {str(email_error)}")
            return {
                "message": "Password updated in DB but notification email failed to dispatch",
                "new_password": new_password
            }

        return {
            "message": "Password has been reset successfully and sent via email",
            "new_password": new_password
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Password reset error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )