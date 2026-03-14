# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .config.settings import settings
from sqlalchemy import text

from .endpoints.register import router as register_router

app = FastAPI(title="Smart Eye API",version="0.1.0",)

app.include_router(register_router)

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