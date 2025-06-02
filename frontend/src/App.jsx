import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import HRDashboard from './pages/HRDashboard';
import JobDashboard from './pages/JobDashboard';
import ApplyPage from './pages/ApplyPage';
import JobListings from './pages/JobListings';
import CandidateStatusPage from './pages/CandidateStatusPage';
import ResumeAnalyzerPage from './pages/ResumeAnalyzerPage';
// import InterviewPage from './pages/InterviewPage' // To be created
import './App.css';

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/jobs" className="nav-link">Browse Jobs</Link>
        <Link to="/hr" className="nav-link">HR Dashboard</Link>
        <Link to="/analyze-resumes" className="nav-link">Analyze Resumes</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/hr" element={<HRDashboard />} />
        <Route path="/jobs" element={<JobListings />} />
        <Route path="/dashboard/:jobId" element={<JobDashboard />} />
        <Route path="/apply/:jobId" element={<ApplyPage />} />
        <Route path="/candidate-status" element={<CandidateStatusPage />} />
        <Route path="/analyze-resumes" element={<ResumeAnalyzerPage />} />
        {/* <Route path="/interview/:candidateId" element={<InterviewPage />} /> */}
      </Routes>
    </div>
  );
}

export default App; 