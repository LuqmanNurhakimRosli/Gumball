from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    required_skills = Column(Text)
    min_experience = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String) # Foreign key implicit
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    resume_path = Column(String) # Path to stored resume file
    extracted_skills = Column(Text, nullable=True)
    extracted_experience = Column(Text, nullable=True)
    extracted_education = Column(Text, nullable=True)
    ai_score = Column(Float, nullable=True)
    ai_status = Column(String, nullable=True) # e.g., Top Fit, Potential Fit, Flagged
    interview_stage = Column(String, default="Applied") # e.g., Applied, Interview Sent, Interview Complete, Hired, Rejected
    created_at = Column(DateTime, default=datetime.utcnow)

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String) # Foreign key implicit
    question_number = Column(Integer)
    answer_text = Column(Text, nullable=True)
    answer_video_url = Column(String, nullable=True) # For future video support
    ai_analysis = Column(Text, nullable=True)
    ai_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 