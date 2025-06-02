# schemas.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Job Schemas ---

class JobBase(BaseModel):
    title: str
    description: str
    requirements: str
    location: str
    salary_range: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str
    created_at: datetime
    status: str

    class Config:
        from_attributes = True

# --- Candidate Schemas ---

class CandidateBase(BaseModel):
    name: str
    email: str
    phone: str
    job_id: str

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: str
    created_at: datetime
    status: str
    resume_path: Optional[str] = None
    ai_score: Optional[float] = None
    ai_analysis: Optional[str] = None

    class Config:
        from_attributes = True

# --- Interview Schemas ---

class InterviewAnswerBase(BaseModel):
    question: str
    answer: str
    candidate_id: str

class InterviewAnswerCreate(InterviewAnswerBase):
    pass

class InterviewAnswer(InterviewAnswerBase):
    id: str
    created_at: datetime
    ai_analysis: Optional[str] = None

    class Config:
        from_attributes = True

class InterviewAnalysis(BaseModel):
    candidate_id: str
    summary: str
    overall_score: float
    # Add other analysis details as needed

# --- Dashboard Schemas ---

class CandidateStatusCounts(BaseModel):
    total: int
    new: int
    screening: int
    interview: int
    offered: int
    hired: int
    rejected: int

class CandidateRanked(BaseModel):
    id: str
    name: str
    email: str
    ai_score: Optional[float]
    ai_status: Optional[str]
    interview_stage: str

    class Config:
        orm_mode = True

class JobDashboard(BaseModel):
    job: Job
    candidates: List[Candidate]

class DashboardStats(BaseModel):
    total_candidates: int
    top_fit_count: int
    potential_fit_count: int
    flagged_count: int
    applied_count: int
    interview_sent_count: int
    interview_complete_count: int
    # Add more stats as needed

# --- Authentication Schemas (Basic) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str 