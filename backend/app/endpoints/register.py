from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

from ..database import get_db
from ..models.emergency_responder import EmergencyResponder, ApprovalStatus, ActiveStatus
from ..schemas.responder import ResponderCreate, ResponderOut

router = APIRouter(
    prefix="/register",
    tags=["Registration"],
    redirect_slashes=False,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=ResponderOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_responder(
    responder: ResponderCreate,
    db: Session = Depends(get_db)
):
    try:

        responder_id = responder.responder_id.strip()
        full_name = responder.full_name.strip()
        email = responder.email.strip().lower()
        contact_number = responder.contact_number.strip() if responder.contact_number else None

        existing = db.query(EmergencyResponder).filter(
            (EmergencyResponder.responder_id == responder_id) |
            (EmergencyResponder.email == email)
        ).first()

        if existing:
            field = "Responder ID" if existing.responder_id == responder_id else "Email"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field} already registered"
            )

        hashed_password = pwd_context.hash(responder.password)

        new_responder = EmergencyResponder(
            responder_id=responder_id,
            full_name=full_name,
            contact_number=contact_number,
            email=email,
            hashed_password=hashed_password,
            approval_status=ApprovalStatus.PENDING,
            is_active=ActiveStatus.ACTIVE,
            fcm_token=None
        )

        db.add(new_responder)
        db.commit()
        db.refresh(new_responder)

        return new_responder

    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )