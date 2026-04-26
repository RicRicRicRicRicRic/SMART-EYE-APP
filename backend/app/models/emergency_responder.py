from sqlalchemy import Column, String, Enum as SQLEnum, DateTime
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
    __tablename__ = "Emergency_Responders"

    responder_id = Column(String(100), primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    fcm_token = Column(String(255), nullable=True)
    
    approval_status = Column(
        SQLEnum(
            ApprovalStatus,
            values_callable=lambda x: [e.value for e in x],  
        ),
        nullable=False,
        default=ApprovalStatus.PENDING
    )
    
    is_active = Column(
        SQLEnum(
            ActiveStatus,
            values_callable=lambda x: [e.value for e in x],  # forces "active" etc.
        ),
        nullable=False,
        default=ActiveStatus.ACTIVE
    )
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )