import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to Talent Acquisition Platform</h1>
      <div className="features">
        <div className="feature-card">
          <h2>For HR Professionals</h2>
          <p>Manage job postings, review applications, and analyze candidate data</p>
          <Link to="/hr" className="cta-button">Go to HR Dashboard</Link>
        </div>
        <div className="feature-card">
          <h2>For Candidates</h2>
          <p>Find and apply for jobs, track your application status</p>
          <Link to="/jobs" className="cta-button">Browse Jobs</Link>
          <Link to="/candidate-status" className="cta-button">Check Application Status</Link>
        </div>
      </div>
    </div>
  );
}

export default Home; 