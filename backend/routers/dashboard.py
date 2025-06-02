# routers/dashboard.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db

router = APIRouter()

@router.get("/test")
def test_dashboard():
    """Test endpoint for dashboard connection"""
    return {
        "status": "success",
        "message": "Dashboard router is working!",
        "data": {
            "test_data": "This is test data from the dashboard"
        }
    }

@router.get("/job/{job_id}", response_model=schemas.JobDashboard)
def get_job_dashboard(job_id: str, db: Session = Depends(get_db)):
    # Get job details
    job = crud.get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get candidates for this job
    candidates = crud.get_candidates_for_job(db, job_id=job_id)
    
    return {
        "job": job,
        "candidates": candidates
    }

@router.get("/stats/{job_id}", response_model=schemas.CandidateStatusCounts)
def get_dashboard_stats(job_id: str, db: Session = Depends(get_db)):
    # Verify job exists
    job = crud.get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return crud.get_candidates_count_by_status(db, job_id=job_id) 