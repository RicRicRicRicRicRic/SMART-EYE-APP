# app/main.py
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer  # Added
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .config.settings import settings
from sqlalchemy import text

from .endpoints.register import router as register_router
from .endpoints.login_auth import router as login_router
from .endpoints.user_info import router as user_router


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") 

app = FastAPI(
    title="Smart Eye API",
    version="0.1.0",
    redirect_slashes=False,  
)

app.include_router(register_router)
app.include_router(login_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {
        "message": "Smart Eye API running",
        "docs": "Visit /docs",
        "test_db": "Check /test-db to verify database connection"
    }

Base.metadata.create_all(bind=engine)

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "status": "Database connected!",
            "result": result,
            "db_url_used": settings.DATABASE_URL.replace(settings.DB_PASSWORD, "*****"),  # hide pw
        }
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}