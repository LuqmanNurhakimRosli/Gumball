# ai_processing.py

import os
import re
from collections import Counter
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import pdfplumber # Import pdfplumber
import docx # Import python-docx
from typing import List

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def parse_resume(resume_path: str) -> str:
    """Parses PDF or DOCX resume and extracts text content."""
    print(f"Parsing resume: {resume_path}")
    text = ""
    try:
        if resume_path.lower().endswith('.pdf'):
            with pdfplumber.open(resume_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        elif resume_path.lower().endswith(('.doc', '.docx')):
            doc = docx.Document(resume_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
        else:
            # Handle other formats or raise an error
            print(f"Unsupported file format: {resume_path}")
            return "Unsupported file format"
    except Exception as e:
        print(f"Error parsing {resume_path}: {str(e)}")
        return f"Error parsing resume: {str(e)}"
    
    return text

def simple_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using basic word overlap."""
    # Convert to lowercase and split into words, removing punctuation
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0

def compare_resume_to_job(job_requirements: str, resume_text: str) -> float:
    """Compares resume text to job requirements using simple text similarity."""
    print("Comparing resume to job requirements (simple similarity)...")
    
    # Split requirements into individual skills/requirements (simple comma split)
    requirements = [req.strip() for req in job_requirements.split(',') if req.strip()]
    
    if not requirements:
        return 0.0 # No requirements to compare
        
    # Calculate average similarity of each requirement against the whole resume text
    similarities = [simple_text_similarity(req, resume_text) for req in requirements]
    
    return np.mean(similarities)

def flag_suspicious_resume(resume_text: str) -> bool:
    """Flags possible fake or suspicious resumes (basic checks)."""
    print("Checking for suspicious resume...")
    
    # Simple checks
    if len(resume_text) < 100:  # Too short (arbitrary threshold)
        return True
    
    # Check for unusually high frequency of any single word (might indicate copy-paste or junk)
    words = re.findall(r'\b\w+\b', resume_text.lower())
    if not words: return False # Avoid division by zero
    word_counts = Counter(words)
    most_common_word_count = word_counts.most_common(1)[0][1] if word_counts else 0
    
    if most_common_word_count > len(words) * 0.15: # If most common word is more than 15% of total words
         print(f"Flagged: Most common word count ({most_common_word_count}) > 15% of total words ({len(words)})")
         return True

    return False

def determine_ai_status(score: float, is_flagged: bool) -> str:
    """Determines candidate AI status based on score and flags."""
    if is_flagged:
        return "Flagged"
    elif score >= 70.0:
        return "Top Fit"
    elif score >= 50.0:
        return "Potential Fit"
    else:
        return "Needs Review"

def analyze_resume(resume_path: str, job_requirements: str) -> tuple[float, str]:
    """
    Analyzes a resume based on job requirements using Gemini AI.
    Returns a tuple of (relevance_score, detailed_analysis).
    Relevance score is from 0-100.
    """
    print(f"Analyzing resume {os.path.basename(resume_path)} against requirements: {job_requirements}")
    try:
        # Parse resume content
        resume_content = parse_resume(resume_path)

        if resume_content.startswith("Error parsing resume") or resume_content.startswith("Unsupported file format"):
             # If parsing failed, return a low score and the error message
             return 0.0, resume_content
        
        # Construct a detailed prompt for Gemini
        prompt = f"""
        You are an AI assistant specialized in analyzing resumes for job applications.
        Your task is to evaluate the following resume based on the provided job requirements.
        
        Job Requirements: {job_requirements}
        
        Resume Content:
        {resume_content}
        
        Based on the job requirements, provide:
        1. A RELEVANCE SCORE from 0 to 100, where 100 is a perfect match.
        2. A DETAILED ANALYSIS explaining why the score was given, highlighting strengths related to requirements and noting any gaps or areas for improvement.
        
        Format your response strictly as follows:
        RELEVANCE SCORE: [number]
        DETAILED ANALYSIS: [Your detailed analysis here]
        """
        
        # Get AI response from Gemini
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        print("Gemini Response:")
        print(response_text)

        # Parse the structured response
        score_match = re.search(r"RELEVANCE SCORE:\s*(\d+\.?\d*)", response_text, re.IGNORECASE)
        analysis_match = re.search(r"DETAILED ANALYSIS:\s*(.*)", response_text, re.IGNORECASE | re.DOTALL)
        
        score = float(score_match.group(1)) if score_match else 0.0
        analysis = analysis_match.group(1).strip() if analysis_match else "AI analysis could not be extracted from response."

        # Basic check for suspicious content (optional, can be integrated differently)
        # is_flagged = flag_suspicious_resume(resume_content)
        # if is_flagged:
        #     analysis = "[FLAGGED AS POTENTIALLY SUSPICIOUS] " + analysis
        
        return score, analysis
    
    except Exception as e:
        print(f"Critical error during resume analysis: {str(e)}")
        return 0.0, f"Critical error during analysis: {str(e)}"

def analyze_interview_answer(answer: str) -> str:
    """
    Analyze an interview answer using Gemini AI.
    Returns the analysis as a string.
    """
    print("Analyzing interview answer...")
    try:
        # Generate prompt for answer analysis
        prompt = f"""
        Analyze this interview answer and provide:
        1. A detailed analysis of the response quality
        2. Key strengths and areas for improvement
        3. Suggestions for better answers
        
        Answer:
        {answer}
        
        Format your response as a detailed analysis.
        """
        
        # Get AI response
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error in interview answer analysis: {str(e)}")
        return "Error analyzing interview answer" 