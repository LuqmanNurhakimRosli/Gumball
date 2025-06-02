import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getJob, getRankedCandidates, getJobStats } from '../api/api';

function JobDashboard() {
  const { jobId } = useParams();
  const [job, setJob] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJobData();
  }, [jobId]);

  const fetchJobData = async () => {
    try {
      const [jobResponse, candidatesResponse, statsResponse] = await Promise.all([
        getJob(jobId),
        getRankedCandidates(jobId),
        getJobStats(jobId)
      ]);

      setJob(jobResponse.data);
      setCandidates(candidatesResponse.data);
      setStats(statsResponse.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) return <div>Loading job dashboard...</div>;
  if (error) return <div>Error loading job dashboard: {error}</div>;
  if (!job) return <div>Job not found</div>;

  return (
    <div className="job-dashboard">
      <h1>Job Dashboard: {job.title}</h1>
      
      <div className="stats-container">
        <div className="stat-card">
          <h3>Total Applications</h3>
          <p className="stat-number">{stats?.total_applications || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Average Score</h3>
          <p className="stat-number">{stats?.average_score?.toFixed(2) || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Top Candidates</h3>
          <p className="stat-number">{stats?.top_candidates || 0}</p>
        </div>
      </div>

      <div className="candidates-section">
        <h2>Ranked Candidates</h2>
        <div className="candidates-list">
          {candidates.map((candidate) => (
            <div key={candidate.id} className="candidate-card">
              <h3>{candidate.name}</h3>
              <p>Email: {candidate.email}</p>
              <p>Score: {candidate.score?.toFixed(2)}</p>
              <p>Status: {candidate.status}</p>
              <div className="candidate-actions">
                <button onClick={() => window.location.href = `/interview/${candidate.id}`}>
                  View Interview
                </button>
                <button onClick={() => window.location.href = `mailto:${candidate.email}`}>
                  Contact
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="job-details">
        <h2>Job Details</h2>
        <p><strong>Title:</strong> {job.title}</p>
        <p><strong>Description:</strong> {job.description}</p>
        <p><strong>Requirements:</strong> {job.requirements}</p>
        <p><strong>Location:</strong> {job.location}</p>
        <p><strong>Salary Range:</strong> {job.salary_range}</p>
        <p><strong>Status:</strong> {job.status}</p>
        <p><strong>Application Link:</strong> <a href={`/apply/${job.id}`}>Apply Here</a></p>
      </div>
    </div>
  );
}

export default JobDashboard; 