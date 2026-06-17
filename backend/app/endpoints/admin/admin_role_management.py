# app/endpoints/admin/admin_role_management.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder, ResponderRole
from ...schemas.admin.admin import StandardResponse

router = APIRouter(prefix="/admin", tags=["Role Management"])

@router.patch("/responders/{responder_id}/promote-to-admin")
async def promote_to_admin(
    responder_id: str,
    db: Session = Depends(get_db)
):
    """Promote Responder → Admin"""
    # Clean the ID to prevent matching failures
    clean_id = responder_id.strip()
    
    responder = db.query(EmergencyResponder).filter(
        EmergencyResponder.responder_id == clean_id
    ).first()

    if not responder:
        # Debug helper: confirms exactly what ID the server is failing to find
        raise HTTPException(
            status_code=404, 
            detail=f"Responder with ID '{clean_id}' not found in database"
        )

    if responder.responder_role == ResponderRole.SUPER_ADMIN:
        raise HTTPException(status_code=400, detail="Cannot modify Super Admin")

    if responder.responder_role == ResponderRole.ADMIN:
        raise HTTPException(status_code=400, detail="User is already an Admin")

    responder.responder_role = ResponderRole.ADMIN
    db.commit()
    db.refresh(responder)

    return {"message": f"{responder.full_name} has been promoted to Admin"}

@router.patch("/responders/{responder_id}/demote-to-responder")
async def demote_to_responder(
    responder_id: str,
    db: Session = Depends(get_db)
):
    """Demote Admin → Responder"""
    # Clean the ID
    clean_id = responder_id.strip()

    responder = db.query(EmergencyResponder).filter(
        EmergencyResponder.responder_id == clean_id
    ).first()

    if not responder:
        raise HTTPException(
            status_code=404, 
            detail=f"Responder with ID '{clean_id}' not found in database"
        )

    if responder.responder_role == ResponderRole.SUPER_ADMIN:
        raise HTTPException(status_code=400, detail="Cannot demote Super Admin")

    if responder.responder_role != ResponderRole.ADMIN:
        raise HTTPException(status_code=400, detail="Only Admins can be demoted")

    responder.responder_role = ResponderRole.RESPONDER
    db.commit()
    db.refresh(responder)

    return {"message": f"{responder.full_name} has been demoted to Responder"}