from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import List, Dict, Any
import ai_processing
import os
from pathlib import Path
import uuid
import shutil

router = APIRouter()

# Define a temporary directory for uploads
# Using a temporary directory helps manage files without cluttering static assets
TEMP_UPLOAD_DIR = Path("backend/temp_uploads")
TEMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/analyze-resumes")
async def analyze_multiple_resumes(
    requirements: str = Form(...), # Add requirements as a form field
    files: List[UploadFile] = File(...)
):
    """
    Receives job requirements and multiple resume files, analyzes them using AI
    based on the requirements, and returns a list of analysis results ranked by AI score.
    """
    results = []
    temp_batch_dir = TEMP_UPLOAD_DIR / str(uuid.uuid4()) # Use a temporary ID for this session
    temp_batch_dir.mkdir(exist_ok=True)

    try:
        for file in files:
            file_path = temp_batch_dir / file.filename
            try:
                # Save the file temporarily
                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)

                # Analyze the resume with requirements
                ai_score, ai_analysis = ai_processing.analyze_resume(str(file_path), requirements)

                results.append({
                    "filename": file.filename,
                    "score": ai_score,
                    "analysis": ai_analysis,
                    "status": ai_processing.determine_ai_status(ai_score, False) # Add AI status based on score
                })

            except Exception as e:
                # Log error for this specific file but continue with others
                print(f"Error processing file {file.filename}: {e}")
                results.append({
                    "filename": file.filename,
                    "score": None, # Indicate failure
                    "analysis": f"Failed to process file: {e}",
                    "status": "Failed"
                })
            finally:
                # Clean up the temporary file immediately after processing
                if file_path.exists():
                    os.remove(file_path)

        # Rank the results by score (descending), putting failed ones at the end
        # Candidates with higher scores appear first. None scores (failures) go to the end.
        ranked_results = sorted(results, key=lambda x: (x['score'] is not None, x['score'] if x['score'] is not None else -1), reverse=True)

        return ranked_results

    finally:
        # Clean up the temporary batch directory after all files are processed
        if temp_batch_dir.exists():
            shutil.rmtree(temp_batch_dir) 