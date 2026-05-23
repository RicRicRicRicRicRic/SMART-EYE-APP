# app/endpoints/admin/admin_auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder, ApprovalStatus, ActiveStatus, ResponderRole
from ...schemas.admin.admin import AdminLoginRequest, AdminLoginResponse
from ...utils.security import create_access_token

router = APIRouter(prefix="/admin", tags=["Admin Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(
    login_data: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    try:
        email = login_data.email.strip().lower()

        admin = db.query(EmergencyResponder).filter(
            EmergencyResponder.email == email
        ).first()

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not pwd_context.verify(login_data.password, admin.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if admin.responder_role not in [ResponderRole.ADMIN, ResponderRole.SUPER_ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have admin access"
            )

        access_token = create_access_token(data={"sub": admin.email})

        return {
            "message": "Login successful",
            "admin": admin,
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Admin login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )