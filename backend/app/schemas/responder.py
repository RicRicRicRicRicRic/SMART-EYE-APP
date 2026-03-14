from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class ResponderCreate(BaseModel):
    responder_id: str = Field(..., min_length=4, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    contact_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)


class ResponderOut(BaseModel):
    id: int
    responder_id: str
    full_name: str
    email: EmailStr
    approval_status: str
    is_active: str
    created_at: datetime

    class Config:
        from_attributes = True