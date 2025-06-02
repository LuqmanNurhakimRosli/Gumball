# routers/interview.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db
import ai_processing

router = APIRouter()

@router.post("/{candidate_id}/answer", response_model=schemas.InterviewAnswer)
def create_interview_answer(
    candidate_id: str,
    answer: schemas.InterviewAnswerCreate,
    db: Session = Depends(get_db)
):
    # Verify candidate exists
    candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Create answer
    db_answer = crud.create_interview_answer(db=db, answer=answer)
    
    try:
        # Process answer with AI
        ai_analysis = ai_processing.analyze_interview_answer(answer.answer)
        crud.update_interview_answer_analysis(
            db=db,
            answer_id=db_answer.id,
            ai_analysis=ai_analysis
        )
    except Exception as e:
        # Log error but continue
        print(f"Error processing interview answer: {str(e)}")
    
    return db_answer

@router.get("/{candidate_id}/answers", response_model=List[schemas.InterviewAnswer])
def read_interview_answers(candidate_id: str, db: Session = Depends(get_db)):
    # Verify candidate exists
    candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return crud.get_interview_answers(db=db, candidate_id=candidate_id)

@router.post("/{candidate_id}")
def submit_interview_answers(
    candidate_id: str,
    answers: List[schemas.InterviewAnswerCreate],
    db: Session = Depends(get_db)
):
    candidate = crud.get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Save answers and trigger analysis
    for answer_data in answers:
        db_answer = crud.create_interview_answer(db, answer_data, candidate_id)

        # Get the corresponding question (simulated)
        questions = ai_processing.get_interview_questions(candidate.job_id) # Assuming questions are job-specific
        question_text = questions[answer_data.question_number - 1] if 0 <= answer_data.question_number - 1 < len(questions) else f"Question {answer_data.question_number}"

        # Perform analysis (this should ideally be async)
        analysis_results = ai_processing.analyze_interview_answer(answer_data.answer_text or "", question_text)

        # Update the answer with analysis results
        crud.update_interview_answer_analysis(
            db=db,
            answer_id=db_answer.id,
            ai_analysis=analysis_results["analysis"],
            ai_score=analysis_results["score"]
        )

    # Update candidate interview stage
    crud.update_candidate_interview_stage(db, candidate_id, "Interview Complete")

    return {"message": "Interview answers submitted and analysis triggered."}

@router.get("/{candidate_id}/score", response_model=List[schemas.InterviewAnswer])
def get_interview_score(candidate_id: str, db: Session = Depends(get_db)):
    # Add dummy authentication check here later
    candidate = crud.get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    answers = crud.get_interview_answers_for_candidate(db, candidate_id)
    return answers 