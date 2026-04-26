from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ResponderCreate(BaseModel):
    responder_id: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    contact_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class ResponderOut(BaseModel):
    responder_id: str         
    full_name: str
    email: EmailStr
    approval_status: str
    is_active: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LoginResponse(BaseModel):
    message: str
    responder: ResponderOut