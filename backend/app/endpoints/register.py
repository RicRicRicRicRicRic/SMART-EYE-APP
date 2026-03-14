from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.emergency_responder import EmergencyResponder, ApprovalStatus
from ..schemas.responder import ResponderCreate, ResponderOut
from passlib.context import CryptContext

router = APIRouter(
    prefix="/register",
    tags=["Registration"],
    responses={401: {"description": "Unauthorized"}},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    "/",
    response_model=ResponderOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new emergency responder (pending approval)"
)
async def register_responder(
    responder: ResponderCreate,
    db: Session = Depends(get_db)
):
    existing_responder = db.query(EmergencyResponder).filter(
        (EmergencyResponder.responder_id == responder.responder_id) |
        (EmergencyResponder.email == responder.email)
    ).first()

    if existing_responder:
        field = "Responder ID" if existing_responder.responder_id == responder.responder_id else "Email"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field} already registered"
        )

    hashed_password = pwd_context.hash(responder.password)

    new_responder = EmergencyResponder(
        responder_id=responder.responder_id.strip(),
        full_name=responder.full_name.strip(),
        contact_number=responder.contact_number.strip() if responder.contact_number else None,
        email=responder.email.strip().lower(),
        hashed_password=hashed_password,
        approval_status=ApprovalStatus.PENDING,
        is_active="active"  
    )

    db.add(new_responder)
    db.commit()
    db.refresh(new_responder)

    return new_responder