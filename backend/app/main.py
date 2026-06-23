# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer  
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .config.settings import settings
from sqlalchemy import text

from .models.emergency_responder import EmergencyResponder
from .models.password_reset import PasswordResetRequest   

from .endpoints.mobile.register import router as register_router
from .endpoints.mobile.login_auth import router as login_router
from .endpoints.mobile.user_info import router as user_router
from .endpoints.mobile.profile_upload import router as profile_upload_router
from .endpoints.mobile.profile_update import router as profile_update_router
from .endpoints.mobile.reset_password_request import router as reset_password_request_router

from .endpoints.admin.admin_auth import router as admin_auth_router
from .endpoints.admin.admin_responders import router as admin_responders_router
from .endpoints.admin.admin_password_reset import router as admin_password_reset_router
from .endpoints.admin.admin_role_management import router as admin_role_management_router

from .endpoints.drone.drone_location import router as drone_location
from .endpoints.drone.drone_status import router as drone_status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") 

app = FastAPI(
    title="Smart Eye API",
    version="0.1.0",
    redirect_slashes=False,  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(register_router)
app.include_router(login_router)
app.include_router(user_router)
app.include_router(profile_upload_router)
app.include_router(profile_update_router)
app.include_router(reset_password_request_router)

app.include_router(admin_auth_router)
app.include_router(admin_responders_router)
app.include_router(admin_password_reset_router)
app.include_router(admin_role_management_router)

app.include_router(drone_location)
app.include_router(drone_status)

@app.get("/")
def read_root():
    return {
        "message": "Smart Eye API running",
        "docs": "Visit /docs",
        "test_db": "Check /test-db to verify database connection"
    }


@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "status": "Database connected!",
            "result": result,
            "db_url_used": settings.DATABASE_URL.replace(settings.DB_PASSWORD, "*****"),  
        }
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}

Base.metadata.create_all(bind=engine)