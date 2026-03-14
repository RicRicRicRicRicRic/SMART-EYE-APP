# main.py (clean version after testing)
from fastapi import FastAPI
from app.config.settings import settings   
from app.endpoints import register
from app.endpoints.register import router as register_router

app = FastAPI(title="SMART-EYE Backend - Incident Alerts")

app.include_router(register.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "SMART-EYE backend is running! Ready for drone alerts."}

@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "SMART-EYE Emergency Response"}