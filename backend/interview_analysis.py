# interview_analysis.py

import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
genai.configure(api_key=GEMINI_API_KEY)



def analyze_interview_answer(answer_text: str, question: str) -> dict:
    """Analyzes interview answer using Gemini API."""
    print(f"Analyzing answer for question: {question}")
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Create prompt for analysis
        prompt = f"""
        Analyze the following interview answer and provide:
        1. A brief summary of the response
        2. A score from 0-1 based on:
           - Relevance to the question
           - Clarity and structure
           - Depth of understanding
           - Professional tone
        
        Question: {question}
        Answer: {answer_text}
        
        Provide the analysis in this format:
        Summary: [your summary]
        Score: [0-1 score]
        """
        
        # Generate response
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Parse the response
        summary = ""
        score = 0.5  # Default score
        
        for line in response_text.split('\n'):
            if line.startswith('Summary:'):
                summary = line.replace('Summary:', '').strip()
            elif line.startswith('Score:'):
                try:
                    score = float(line.replace('Score:', '').strip())
                    # Ensure score is between 0 and 1
                    score = max(0, min(1, score))
                except ValueError:
                    pass
        
        return {
            "summary": summary or "No summary generated",
            "score": score
        }
        
    except Exception as e:
        print(f"Error analyzing answer with Gemini: {e}")
        # Fallback to basic analysis
        return {
            "summary": f"Basic analysis: The candidate provided an answer regarding {question}.",
            "score": len(answer_text) / 500.0  # Simple length-based score
        }

def get_interview_questions(job_id: str) -> List[str]:
    """Retrieves interview questions for a given job."""
    # TODO: Implement logic to fetch or generate job-specific questions
    # For now, return a static list:
    return [
        "Tell me about a time you faced a challenging technical problem and how you solved it.",
        "Describe your experience with the key skills required for this role.",
        "Why are you interested in this position and our company?"
    ] 