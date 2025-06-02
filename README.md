# Talent Acquisition Platform

A modern AI-powered talent acquisition platform built with FastAPI and React.

## Project Flow

Here's the complete intended flow for the talent acquisition process within the platform:

```mermaid
flowchart TD
    A[HR Creates Job & Rules] --> B[System Generates Application Link]
    B --> C[Candidate Applies via Link]
    C --> D[Resume Uploaded & Parsed (Gemini API)]
    D --> E[AI Filtering & Spam Detection]
    E --> F[Shortlist Candidates]
    F --> G[AI Interview Invitation Sent]
    G --> H[Candidate Completes AI Interview]
    H --> I[AI Analyzes Interview (Gemini API)]
    I --> J[HR Dashboard Review]
    J --> K[HR Approves for Live Interview]
    K --> L[Live Interview Scheduled & Notified]
    L --> M[Process Complete & Feedback]
```

**Current Status:** The project is a work in progress. The core functionalities from **A to E** in the flowchart have been implemented, including:

- HR can create job postings with requirements.
- The system generates a unique link for each job application.
- Candidates can access the application page via the link, fill in their details, and upload their resume (PDF/DOCX).
- The system uploads and parses the resume content.
- Basic AI analysis is performed to provide a relevance score and initial analysis based on requirements.

**Further Development Needed:** The system requires significant further development to implement the complete process as outlined in the flowchart.

## Next Steps for Collaboration

This project is now ready for the next phase of development. The primary focus for the next contributor will be to build out the functionalities from **E to L** in the flowchart. This includes:

- **Implementing Candidate Shortlisting (E -> F):** Develop logic to formally 'shortlist' candidates based on AI scores and potentially other criteria, making this status visible on the HR Dashboard.
- **AI Interview Invitation & Process (F -> I):**
    - Implement the functionality to trigger sending AI interview invitations to shortlisted candidates (G).
    - Develop the frontend page and backend endpoints for candidates to complete the AI interview (H), including handling recording/submission of answers.
    - Enhance the AI processing module (`ai_processing.py`) to analyze interview answers (I).
- **HR Dashboard Enhancements (I -> J):** Update the HR Dashboard to display AI interview analysis results alongside resume analysis.
- **Live Interview Scheduling (J -> L):**
    - Implement the functionality for HR to approve candidates for a live interview (K).
    - Develop a system for scheduling live interviews and notifying both HR and the candidate (L).
- **Candidate Status Page:** Enhance the Candidate Status page to show detailed progress through the pipeline (from application received through live interview scheduling).
- **Refine AI Models:** Continuously improve the prompts and potentially integrate more advanced techniques in `ai_processing.py` for better resume and interview analysis.
- **User Authentication and Roles:** Implement proper authentication and differentiate features based on HR and Candidate roles.
- **Error Handling and Edge Cases:** Improve robust error handling throughout the application.
- **Testing:** Write unit and integration tests.

Refer to the existing codebase, particularly the `backend/` and `frontend/` directories, to understand the current implementation and continue building upon it.

## Features

- HR Job Posting
- Candidate Resume Submission
- AI Resume Parsing and Analysis based on Requirements
- Candidate Relevance Scoring and Status
- HR Dashboard (basic view)

## Tech Stack

**Backend:** FastAPI, SQLAlchemy (SQLite), pdfplumber, python-docx, google-generativeai, numpy
**Frontend:** Vite + React, React Router, Axios

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file in the **backend** directory with:
```
GEMINI_API_KEY=your_api_key_here
```

4. Navigate to the frontend directory and install dependencies:
```bash
cd ../frontend
npm install
```

## Running the Application

1. Start the backend server (from the `backend` directory with venv activated):
```bash
uvicorn main:app --reload
```

2. Start the frontend development server (from the `frontend` directory):
```bash
npm run dev
```

3. The frontend will typically be available at http://localhost:5173.
4. The API will be available at http://localhost:8000.
5. API documentation will be available at http://localhost:8000/docs.

## Project Structure

```
.
├── backend/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── jobs.py
│   │   ├── candidates.py
│   │   ├── interview.py
│   │   ├── dashboard.py
│   │   └── ai.py
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   ├── crud.py
│   └── ai_processing.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── HRDashboard.jsx
│   │   │   ├── JobDashboard.jsx
│   │   │   ├── ApplyPage.jsx
│   │   │   ├── JobListings.jsx
│   │   │   ├── CandidateStatusPage.jsx
│   │   │   └── ResumeAnalyzerPage.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.css
│   ├── package.json
│   └── vite.config.js
├── setup.py
├── requirements.txt
└── README.md
```

## API Endpoints

- `POST /jobs/`: Create a new job posting
- `POST /candidates/apply/{job_id}`: Submit a candidate application with resume
- `GET /dashboard/{job_id}`: Get ranked candidates for a job
- `GET /candidates/{id}`: Get detailed candidate info
- `POST /interview/{candidate_id}`: Submit interview answers
- `GET /interview/{candidate_id}/score`: Get interview analysis and score
- `GET /dashboard/{job_id}/stats`: Get job dashboard statistics

## Frontend Routes

- `/hr`: HR dashboard to see created jobs
- `/dashboard/:jobId`: Lists ranked candidates + scores for a specific job
- `/apply/:jobId`: Candidate resume upload page
- `/interview/:candidateId`: Page for candidates to submit interview answers (to be implemented)

## TODOs

- Implement resume parsing logic in `ai_processing.py`.
- Implement semantic similarity and flagging logic in `ai_processing.py`.
- Implement AI interview analysis in `interview_analysis.py`.
- Develop the frontend components and pages.
- Add proper error handling.
- Implement dummy authentication for HR routes.
- Implement email simulation/sending.
- Add charting to the dashboard.
- Refine AI scoring and ranking logic. 