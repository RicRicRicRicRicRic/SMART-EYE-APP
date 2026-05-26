# app/endpoints/admin/admin_responders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder, ApprovalStatus, ActiveStatus
from ...schemas.admin.admin import (
    ResponderListOut, 
    ResponderStatusUpdate, 
    ResponderListResponse
)

router = APIRouter(prefix="/admin", tags=["Admin Responders"])


@router.get("/responders", response_model=ResponderListResponse)
async def get_all_responders(db: Session = Depends(get_db)):
    """Get all responders with stats"""
    responders = db.query(EmergencyResponder).all()

    total = len(responders)
    pending = len([r for r in responders if r.approval_status == ApprovalStatus.PENDING])
    approved = len([r for r in responders if r.approval_status == ApprovalStatus.APPROVED])

    return {
        "responders": responders,
        "total": total,
        "pending": pending,
        "approved": approved
    }


@router.patch("/responders/{responder_id}/status", response_model=ResponderListOut)
async def update_responder_status(
    responder_id: str,
    status_update: ResponderStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update approval status or active status of a responder"""
    responder = db.query(EmergencyResponder).filter(
        EmergencyResponder.responder_id == responder_id
    ).first()

    if not responder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Responder not found"
        )

    if status_update.approval_status is not None:
        responder.approval_status = status_update.approval_status

    if status_update.is_active is not None:
        responder.is_active = status_update.is_active

    db.commit()
    db.refresh(responder)

    return responder


@router.get("/responders/stats")
async def get_responders_stats(db: Session = Depends(get_db)):
    """Get quick stats"""
    total = db.query(EmergencyResponder).count()
    pending = db.query(EmergencyResponder).filter(
        EmergencyResponder.approval_status == ApprovalStatus.PENDING
    ).count()
    approved = db.query(EmergencyResponder).filter(
        EmergencyResponder.approval_status == ApprovalStatus.APPROVED
    ).count()

    return {
        "total": total,
        "pending": pending,
        "approved": approved
    }