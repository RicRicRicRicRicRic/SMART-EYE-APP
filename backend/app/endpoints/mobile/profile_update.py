# app/endpoints/mobile/profile_update.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder
from .user_info import get_current_user
from ...utils.security import create_access_token, pwd_context

router = APIRouter(prefix="/me", tags=["Profile"])


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


@router.put("", status_code=status.HTTP_200_OK)
async def update_profile(
    update_data: ProfileUpdate,
    current_user: EmergencyResponder = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        email_changed = False

        if update_data.full_name is not None:
            current_user.full_name = update_data.full_name.strip()

        if update_data.contact_number is not None:
            current_user.contact_number = update_data.contact_number.strip() if update_data.contact_number.strip() else None

        if update_data.email is not None and update_data.email.lower() != current_user.email:
            existing = db.query(EmergencyResponder).filter(
                EmergencyResponder.email == update_data.email.lower(),
                EmergencyResponder.responder_id != current_user.responder_id
            ).first()
            if existing:
                raise HTTPException(400, detail="Email already in use")

            current_user.email = update_data.email.lower()
            email_changed = True

        if update_data.password is not None and update_data.password.strip():
            if len(update_data.password) < 8:
                raise HTTPException(400, detail="Password must be at least 8 characters")
            current_user.hashed_password = pwd_context.hash(update_data.password)

        db.commit()
        db.refresh(current_user)

        response = {
            "message": "Profile updated successfully",
            "user": current_user
        }

        # Return new token if email changed
        if email_changed:
            new_token = create_access_token(data={"sub": current_user.email})
            response["access_token"] = new_token
            response["token_type"] = "bearer"

        return response

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")