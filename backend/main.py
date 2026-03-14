from fastapi import FastAPI

# This is the correct import based on your folder structure
from app.endpoints.register import router as register_router

app = FastAPI(
    title="SMART-EYE Backend - Incident Alerts",
    description="Receives emergency alerts from drone and serves to mobile app",
    version="0.1.0"
)

# Include the registration router
# Choose ONE of the two lines below — I recommend the second one (with prefix)

# Option A: no prefix → endpoint becomes http://localhost:8000/register
# app.include_router(register_router)

# Option B: with /api/v1 prefix (cleaner, more standard) → endpoint becomes /api/v1/register
app.include_router(register_router, prefix="/api/v1", tags=["registration"])

# Your existing routes
@app.get("/")
def read_root():
    return {"message": "SMART-EYE backend is running! Ready for drone alerts."}

@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "SMART-EYE Emergency Response"}