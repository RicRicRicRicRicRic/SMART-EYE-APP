#app/endpoints/mobile/reset_password_request.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
import logging
from datetime import datetime, timedelta

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder
from ...models.password_reset import PasswordResetRequest, ResetStatus

router = APIRouter(prefix="/password-reset", tags=["Password Reset"])
logger = logging.getLogger(__name__)


@router.post("/request", status_code=status.HTTP_200_OK)
async def request_password_reset(
    email_data: dict,
    db: Session = Depends(get_db)
):
    email = email_data.get("email", "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user = db.query(EmergencyResponder).filter(EmergencyResponder.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Email not found! Please check your email or register first."
        )

    request_id = str(uuid.uuid4())

    reset_request = PasswordResetRequest(
        request_id=request_id,
        responder_id=user.responder_id,
        status=ResetStatus.PENDING,
        expires_at=datetime.utcnow() + timedelta(hours=48)  
    )

    db.add(reset_request)
    db.commit()

    logger.info(f"Password reset request created for {email} (ID: {request_id})")

    return {
        "message": "Your password reset request has been sent to the admin. You will be notified once approved.",
        "request_id": request_id
    }