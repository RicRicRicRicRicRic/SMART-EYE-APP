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
    alphabet = string.ascii_letters + string.digits + "!@#$%^*"
    return ''.join(secrets.choice(alphabet) for i in range(length))

@router.get("/password-reset/requests", response_model=List[dict])
async def get_password_reset_requests(db: Session = Depends(get_db)):
    """Fetch and list pending password reset submissions"""
    try:
        results = db.query(
            ResetModel,
            EmergencyResponder.full_name,
            EmergencyResponder.email
        ).join(
            EmergencyResponder, 
            ResetModel.responder_id == EmergencyResponder.responder_id
        ).all()

        formatted_requests = []
        for reset_req, full_name, email in results:
            formatted_requests.append({
                "request_id": reset_req.request_id,
                "responder_id": reset_req.responder_id,
                "status": reset_req.status,
                "request_date": reset_req.request_date.isoformat() if reset_req.request_date else None,
                "expires_at": reset_req.expires_at.isoformat() if reset_req.expires_at else None,
                "full_name": full_name,
                "email": email
            })
        return formatted_requests
    except Exception as e:
        logging.error(f"Error fetching password reset requests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error during request fetching: {str(e)}"
        )

@router.post("/password-reset/approve/{request_id}")
async def approve_password_reset(request_id: str, db: Session = Depends(get_db)):
    """Approve a password reset request, generate random password, and email it"""
    try:
        reset_request = db.query(ResetModel).filter(ResetModel.request_id == request_id).first()
        if not reset_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password reset request not found"
            )

        if reset_request.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This request has already been processed with status: {reset_request.status}"
            )

        responder = db.query(EmergencyResponder).filter(
            EmergencyResponder.responder_id == reset_request.responder_id
        ).first()

        if not responder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Responder associated with this request not found"
            )

        new_password = generate_random_password()
        responder.hashed_password = pwd_context.hash(new_password)
        reset_request.status = "completed"

        # Email notification dispatch setup
        try:
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            sender_email = os.getenv("SMTP_EMAIL")
            sender_password = os.getenv("SMTP_PASSWORD")

            if not sender_email or not sender_password:
                raise Exception("SMTP credentials are misconfigured or missing in .env environment")

            message_body = f"""
Dear {responder.full_name},

Your SMART-EYE administrative password reset request has been approved.
Your new temporary password is: {new_password}

Please log in to your account using this temporary credential and change your password immediately within your account dashboard settings.
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
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Password not updated. Email dispatch failed: {str(email_error)}"
            )

        # Commit changes to DB only if the email dispatch goes through smoothly
        db.commit()
        db.refresh(responder)

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
            detail=f"Internal error during credential resolution processing: {str(e)}"
        )

@router.post("/password-reset/reject/{request_id}")
async def reject_password_reset(request_id: str, db: Session = Depends(get_db)):
    """Reject a password reset request and set its status to cancelled"""
    try:
        reset_request = db.query(ResetModel).filter(ResetModel.request_id == request_id).first()
        if not reset_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password reset request not found"
            )

        if reset_request.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This request has already been processed with status: {reset_request.status}"
            )

        # Set status to cancelled as requested
        reset_request.status = "cancelled"
        db.commit()

        return {
            "message": "Password reset request has been rejected and cancelled successfully."
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error rejecting password request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error during rejection processing: {str(e)}"
        )