# app/endpoints/mobile/profile_update.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder
from .user_info import get_current_user
from passlib.context import CryptContext

router = APIRouter(prefix="/me", tags=["Profile"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    contact_number: str | None = None
    email: EmailStr | None = None
    password: str | None = None


@router.put("/", status_code=status.HTTP_200_OK)
async def update_profile(
    update_data: ProfileUpdate,
    current_user: EmergencyResponder = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if update_data.full_name is not None:
            current_user.full_name = update_data.full_name.strip()

        if update_data.contact_number is not None:
            current_user.contact_number = update_data.contact_number.strip() if update_data.contact_number.strip() else None

        if update_data.email is not None:
            existing = db.query(EmergencyResponder).filter(
                EmergencyResponder.email == update_data.email.lower(),
                EmergencyResponder.responder_id != current_user.responder_id
            ).first()
            if existing:
                raise HTTPException(400, detail="Email already in use")
            current_user.email = update_data.email.lower()

        if update_data.password is not None:
            if len(update_data.password) < 8:
                raise HTTPException(400, detail="Password must be at least 8 characters")
            current_user.hashed_password = pwd_context.hash(update_data.password)

        db.commit()
        db.refresh(current_user)

        return {
            "message": "Profile updated successfully",
            "user": current_user
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update profile")