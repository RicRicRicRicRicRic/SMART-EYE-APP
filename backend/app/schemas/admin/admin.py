# app/schemas/admin/admin.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

from app.models.emergency_responder import (
    ApprovalStatus, 
    ActiveStatus, 
    ResponderRole
)

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class AdminLoginResponse(BaseModel):
    message: str
    admin: "ResponderListOut"   
    access_token: str
    token_type: str = "bearer"

class ResponderListOut(BaseModel):
    responder_id: str
    full_name: str
    email: EmailStr
    contact_number: Optional[str] = None
    profile_picture_url: Optional[str] = None
    responder_role: ResponderRole
    approval_status: ApprovalStatus
    is_active: ActiveStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResponderStatusUpdate(BaseModel):
    approval_status: Optional[ApprovalStatus] = None
    is_active: Optional[ActiveStatus] = None


class ResponderDetailOut(ResponderListOut):
    """Extended version if needed"""
    pass

class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    message: str
    new_password: Optional[str] = None   

class StandardResponse(BaseModel):
    message: str
    success: bool = True


class ResponderListResponse(BaseModel):
    responders: List[ResponderListOut]
    total: int
    pending: int
    approved: int

AdminLoginResponse.model_rebuild()