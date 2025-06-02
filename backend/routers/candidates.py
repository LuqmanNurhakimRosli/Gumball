# routers/candidates.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db
import ai_processing
import os
from pathlib import Path

router = APIRouter()

# Define upload directory
UPLOAD_DIR = Path("backend/static/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Endpoint to create a candidate (might be used internally or by HR)
@router.post("/", response_model=schemas.Candidate)
async def create_candidate_internal(
    candidate: schemas.CandidateCreate,
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # This endpoint is kept for potential internal use, but application submission
    # should go through the /apply/{job_id} endpoint below.

    # Verify job exists
    job = crud.get_job(db, job_id=candidate.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Create job-specific directory
    job_dir = UPLOAD_DIR / candidate.job_id
    job_dir.mkdir(exist_ok=True)
    
    # Save resume
    resume_path = job_dir / resume.filename
    with open(resume_path, "wb") as f:
        content = await resume.read()
        f.write(content)
    
    # Create candidate
    db_candidate = crud.create_candidate(db=db, candidate=candidate)
    
    try:
        # Process resume with AI
        ai_score, ai_analysis = ai_processing.analyze_resume(str(resume_path))
        crud.update_candidate_ai_analysis(
            db=db,
            candidate_id=db_candidate.id,
            ai_score=ai_score,
            ai_analysis=ai_analysis
        )
    except Exception as e:
        # Log error but continue
        print(f"Error processing resume: {str(e)}")
    
    return db_candidate

# Endpoint for candidates to apply for a specific job
@router.post("/apply/{job_id}", response_model=schemas.Candidate)
async def apply_for_job_endpoint(
    job_id: str,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verify job exists
    job = crud.get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Create job-specific directory
    job_dir = UPLOAD_DIR / job_id
    job_dir.mkdir(exist_ok=True)
    
    # Save resume
    resume_path = job_dir / resume.filename
    try:
        with open(resume_path, "wb") as f:
            content = await resume.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save resume file: {e}")
    
    # Create candidate schema object
    candidate_create = schemas.CandidateCreate(
        name=name,
        email=email,
        phone=phone,
        resume_path=str(resume_path), # Store the path in the database
        job_id=job_id
    )

    # Create candidate in DB
    db_candidate = crud.create_candidate(db=db, candidate=candidate_create)
    
    try:
        # Process resume with AI
        ai_score, ai_analysis = ai_processing.analyze_resume(str(resume_path))
        crud.update_candidate_ai_analysis(
            db=db,
            candidate_id=db_candidate.id,
            ai_score=ai_score,
            ai_analysis=ai_analysis
        )
    except Exception as e:
        # Log error but continue, maybe set a status indicating AI processing failed
        print(f"Error processing resume for candidate {db_candidate.id}: {str(e)}")
        # Optionally update candidate status to indicate processing failed
        # crud.update_candidate_status(db, db_candidate.id, "AI Processing Failed")
    
    return db_candidate

@router.get("/job/{job_id}", response_model=List[schemas.Candidate])
def read_candidates_for_job(job_id: str, db: Session = Depends(get_db)):
    # Verify job exists
    job = crud.get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return crud.get_candidates_for_job(db=db, job_id=job_id)

@router.get("/{candidate_id}", response_model=schemas.Candidate)
def read_candidate(candidate_id: str, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

@router.put("/{candidate_id}/status")
def update_candidate_status(
    candidate_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    db_candidate = crud.update_candidate_status(db, candidate_id=candidate_id, status=status)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Status updated successfully"}

# Endpoint to send interview link (simulated)
@router.post("/{candidate_id}/send-interview")
def send_interview_link(candidate_id: str, db: Session = Depends(get_db)):
    # Add dummy authentication check here later
    candidate = crud.get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    if candidate.ai_status != "Top Fit":
         raise HTTPException(status_code=400, detail="Can only send interview to Top Fit candidates")

    # TODO: Simulate sending email with a link to frontend interview page
    interview_link = f"/interview/{candidate_id}" # Example frontend route
    print(f"Simulating sending interview email to {candidate.email} with link: {interview_link}")

    # Update candidate stage
    crud.update_candidate_interview_stage(db, candidate_id, "Interview Sent")

    return {"message": f"Interview link simulated sent to {candidate.email}", "link": interview_link} 