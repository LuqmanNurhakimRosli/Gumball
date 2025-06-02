# main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine
from routers import jobs, candidates, interview, dashboard, ai

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Talent Acquisition Platform API")

# Configure CORS - More permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(candidates.router, prefix="/api/candidates", tags=["candidates"])
app.include_router(interview.router, prefix="/api/interview", tags=["interview"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Talent Acquisition Platform API"}

@app.get("/api/test")
def test_endpoint():
    """Test endpoint for frontend connection"""
    return {
        "status": "success",
        "message": "Backend is connected!",
        "data": {
            "timestamp": "2024-03-19T12:00:00Z",
            "version": "1.0.0"
        }
    }

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "detail": "Internal server error"
        }
    ) 