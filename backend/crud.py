# crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from database import Job, Candidate, InterviewAnswer
import schemas
import uuid
from typing import List, Dict

def get_job(db: Session, job_id: str):
    return db.query(Job).filter(Job.id == job_id).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()

def create_job(db: Session, job: schemas.JobCreate):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_candidate(db: Session, candidate_id: str):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def get_candidates_for_job(db: Session, job_id: str):
    return db.query(Candidate).filter(Candidate.job_id == job_id).all()

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def update_candidate_status(db: Session, candidate_id: str, status: str):
    candidate = get_candidate(db, candidate_id)
    if candidate:
        candidate.status = status
        db.commit()
        db.refresh(candidate)
    return candidate

def update_candidate_ai_analysis(db: Session, candidate_id: str, ai_score: float, ai_analysis: str):
    candidate = get_candidate(db, candidate_id)
    if candidate:
        candidate.ai_score = ai_score
        candidate.ai_analysis = ai_analysis
        db.commit()
        db.refresh(candidate)
    return candidate

def create_interview_answer(db: Session, answer: schemas.InterviewAnswerCreate):
    db_answer = InterviewAnswer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_interview_answers(db: Session, candidate_id: str):
    return db.query(InterviewAnswer).filter(InterviewAnswer.candidate_id == candidate_id).all()

def update_interview_answer_analysis(db: Session, answer_id: str, ai_analysis: str):
    answer = db.query(InterviewAnswer).filter(InterviewAnswer.id == answer_id).first()
    if answer:
        answer.ai_analysis = ai_analysis
        db.commit()
        db.refresh(answer)
    return answer

def get_candidates_count_by_status(db: Session, job_id: str):
    counts = db.query(
        Candidate.status,
        func.count(Candidate.id)
    ).filter(
        Candidate.job_id == job_id
    ).group_by(
        Candidate.status
    ).all()
    
    # Initialize counts with 0
    status_counts = {
        "total": 0,
        "new": 0,
        "screening": 0,
        "interview": 0,
        "offered": 0,
        "hired": 0,
        "rejected": 0
    }
    
    # Update counts from database
    for status, count in counts:
        status_counts[status] = count
        status_counts["total"] += count
    
    return status_counts 