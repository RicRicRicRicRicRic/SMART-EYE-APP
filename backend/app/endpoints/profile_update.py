# app/endpoints/profile_update.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models.emergency_responder import EmergencyResponder
from ..endpoints.user_info import get_current_user

router = APIRouter(prefix="/me", tags=["Profile"])


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    contact_number: str | None = None


@router.put("", status_code=status.HTTP_200_OK)
async def update_profile(
    update_data: ProfileUpdate,
    current_user: EmergencyResponder = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if update_data.full_name:
            current_user.full_name = update_data.full_name.strip()
        
        if update_data.contact_number is not None:
            current_user.contact_number = update_data.contact_number.strip() if update_data.contact_number.strip() else None

        db.commit()
        db.refresh(current_user)

        return {
            "message": "Profile updated successfully",
            "user": current_user
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update profile")