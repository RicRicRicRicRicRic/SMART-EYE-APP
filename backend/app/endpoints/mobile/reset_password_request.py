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

    # Check if the user already has a pending password reset request
    existing_request = db.query(PasswordResetRequest).filter(
        PasswordResetRequest.responder_id == user.responder_id,
        PasswordResetRequest.status == ResetStatus.PENDING
    ).first()

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A password reset request is already pending approval. Please wait for an administrator to process it."
        )

    request_id = str(uuid.uuid4())

    # Ensures timestamp is stored cleanly
    reset_request = PasswordResetRequest(
        request_id=request_id,
        responder_id=user.responder_id,
        status=ResetStatus.PENDING,
        request_date=datetime.utcnow(),  
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )

    try:
        db.add(reset_request)
        db.commit()
        db.refresh(reset_request)
        
        logger.info(f"Password reset request registered successfully for tracking: {request_id}")
        return {
            "message": "Your password reset request has been submitted to administrators for verification.",
            "request_id": request_id
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Database insertion failed for reset token tracker: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register password reset request configuration."
        )