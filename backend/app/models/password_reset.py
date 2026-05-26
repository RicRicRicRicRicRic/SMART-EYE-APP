from sqlalchemy import Column, String, Enum as SQLEnum, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base
import enum


class ResetStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PasswordResetRequest(Base):
    __tablename__ = "Password_Reset_Requests"

    request_id = Column(String(100), primary_key=True, index=True)
    
    responder_id = Column(
        String(100), 
        ForeignKey("Emergency_Responders.responder_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    status = Column(
        SQLEnum(ResetStatus),
        nullable=False,
        default=ResetStatus.PENDING
    )
    
    request_date = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    expires_at = Column(DateTime(timezone=True), nullable=True)