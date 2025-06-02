// api.js

import axios from 'axios';

export const API_URL = 'http://127.0.0.1:8000/api'; // Added /api prefix and export

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    // Add any authentication headers here later
  },
});

// --- Job Endpoints ---

export const createJob = (jobData) => {
  // jobData: { title, required_skills, min_experience }
  return api.post('/jobs/', jobData);
};

export const getJobs = () => {
  return api.get('/jobs/');
};

export const getJob = (jobId) => {
  return api.get(`/jobs/${jobId}`);
};

// --- Candidate Endpoints ---

export const applyForJob = (jobId, formData) => {
  // formData: FormData object containing { name, email, phone, resume_file }
  // Headers need to be adjusted for FormData
   return axios.post(`${API_URL}/candidates/apply/${jobId}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

export const getCandidate = (candidateId) => {
  return api.get(`/candidates/${candidateId}`);
};

export const sendInterviewLink = (candidateId) => {
  return api.post(`/candidates/${candidateId}/send-interview`);
};

// --- Interview Endpoints ---

export const submitInterviewAnswers = (candidateId, answers) => {
  // answers: Array of { question_number, answer_text, answer_video_url }
  return api.post(`/interview/${candidateId}`, answers);
};

export const getInterviewScore = (candidateId) => {
  return api.get(`/interview/${candidateId}/score`);
};

// --- Dashboard Endpoints ---

export const getRankedCandidates = (jobId) => {
  return api.get(`/dashboard/job/${jobId}`);  // Updated to match backend route
};

export const getJobStats = (jobId) => {
  return api.get(`/dashboard/stats/${jobId}`);  // Updated to match backend route
};

// --- Auth Endpoints (Dummy) ---
// export const login = (credentials) => {
//   return api.post('/token', credentials); // Example endpoint
// }; 