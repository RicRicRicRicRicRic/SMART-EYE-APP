# app/models/emergency_responder.py
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from ..database import Base
import enum


class ApprovalStatus(str, enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class ActiveStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class EmergencyResponder(Base):
    __tablename__ = "emergency_responders"

    id = Column(Integer, primary_key=True, index=True)
    responder_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    fcm_token = Column(String(255), nullable=True)
    approval_status = Column(
        Enum(ApprovalStatus),
        nullable=False,
        default=ApprovalStatus.PENDING
    )
    is_active = Column(
        Enum(ActiveStatus),
        nullable=False,
        default=ActiveStatus.ACTIVE
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )