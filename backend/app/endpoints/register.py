from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models import EmergencyResponder

# Password hashing (bcrypt — secure and standard)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    responder_id: str
    full_name: str
    contact_number: Optional[str] = None
    email: EmailStr
    password: str


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):
    # 1. Check for duplicates (responder_id is UNIQUE in DB, email we also protect)
    if db.query(EmergencyResponder).filter(EmergencyResponder.responder_id == user.responder_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Responder ID already exists"
        )

    if db.query(EmergencyResponder).filter(EmergencyResponder.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Hash the password
    hashed_password = pwd_context.hash(user.password)

    # 3. Create the new responder (approval_status = Pending by design)
    new_responder = EmergencyResponder(
        responder_id=user.responder_id,
        full_name=user.full_name,
        contact_number=user.contact_number.strip() if user.contact_number else None,
        email=user.email,
        hashed_password=hashed_password,
        # fcm_token remains NULL (will be set later)
        approval_status="Pending",
        is_active="active",
    )

    db.add(new_responder)
    db.commit()
    db.refresh(new_responder)

    return {"message": "Registration submitted! Waiting for approval."}