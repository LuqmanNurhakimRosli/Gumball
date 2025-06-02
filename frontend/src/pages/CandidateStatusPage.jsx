import React, { useState } from 'react';

function CandidateStatusPage() {
  const [email, setEmail] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [applicationStatus, setApplicationStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheckStatus = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setApplicationStatus(null);

    // TODO: Implement backend API call to check status
    console.log(`Checking status for email: ${email}, job title: ${jobTitle}`);

    // Dummy data for now
    setTimeout(() => {
      setLoading(false);
      // Example success
      // setApplicationStatus({ status: 'Under Review', job_title: jobTitle });
      // Example not found
       setError('Application not found. Please double-check your details.');
    }, 1000);
  };

  return (
    <div className="candidate-status-page">
      <h1>Check Application Status</h1>
      <p>Enter your email and the job title you applied for to check your application status.</p>

      <form onSubmit={handleCheckStatus} className="status-form">
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="jobTitle">Job Title Applied For</label>
          <input
            type="text"
            id="jobTitle"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Checking...' : 'Check Status'}
        </button>
      </form>

      {error && (
        <div className="error-message">{error}</div>
      )}

      {applicationStatus && (
        <div className="status-result">
          <h2>Status for "{applicationStatus.job_title}"</h2>
          <p>Current Status: <strong>{applicationStatus.status}</strong></p>
          {/* Add more details here if available from backend */}
        </div>
      )}
    </div>
  );
}

export default CandidateStatusPage; 