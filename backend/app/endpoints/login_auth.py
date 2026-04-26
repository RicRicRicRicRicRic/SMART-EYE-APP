#app/endpoints/login_auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

from ..database import get_db
from ..models.emergency_responder import EmergencyResponder, ApprovalStatus, ActiveStatus
from ..schemas.responder import LoginRequest, LoginResponse

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
    redirect_slashes=False,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)


@router.post("", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_responder(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        email = login_data.email.strip().lower()

        user = db.query(EmergencyResponder).filter(
            EmergencyResponder.email == email
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if user.approval_status != ApprovalStatus.APPROVED:
            if user.approval_status == ApprovalStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your account is pending admin approval. Please wait."
                )
            else: 
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your account has been rejected by the admin."
                )


        if user.is_active != ActiveStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is inactive or suspended."
            )

        if not pwd_context.verify(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful",
            "responder": user  
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )