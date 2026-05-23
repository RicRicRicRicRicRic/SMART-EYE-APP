#app/endpoints/mobile/user_info.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder
from ...schemas.mobile.responder import ResponderOut   # Make sure this is imported
from ...utils.security import verify_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/me",
    tags=["User"],
    redirect_slashes=False,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
logger = logging.getLogger(__name__)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(EmergencyResponder).filter(EmergencyResponder.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


@router.get("", response_model=ResponderOut)
async def get_user_info(current_user: EmergencyResponder = Depends(get_current_user)):
    return current_user