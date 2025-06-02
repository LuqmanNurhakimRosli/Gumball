import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getJobs, createJob } from '../api/api';

function HRDashboard() {
  const [jobs, setJobs] = useState([]);
  const [newJob, setNewJob] = useState({
    title: '',
    description: '',
    requirements: '',
    location: '',
    salary_range: '',
    opening_date: '',
    closing_date: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [stats, setStats] = useState({
    totalJobs: 0,
    activeJobs: 0,
    totalApplications: 0,
    upcomingJobs: 0
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await getJobs();
      const currentDate = new Date();
      const jobsData = response.data.map(job => ({
        ...job,
        status: getJobStatus(job.opening_date, job.closing_date)
      }));
      
      setJobs(jobsData);
      // Calculate stats
      setStats({
        totalJobs: jobsData.length,
        activeJobs: jobsData.filter(job => job.status === 'open').length,
        totalApplications: jobsData.reduce((acc, job) => acc + (job.applications_count || 0), 0),
        upcomingJobs: jobsData.filter(job => job.status === 'upcoming').length
      });
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const getJobStatus = (openingDate, closingDate) => {
    const now = new Date();
    const opening = new Date(openingDate);
    const closing = new Date(closingDate);

    if (now < opening) return 'upcoming';
    if (now > closing) return 'closed';
    return 'open';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-MY', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewJob(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCreateJob = async (e) => {
    e.preventDefault();
    try {
      const response = await createJob(newJob);
      const jobWithStatus = {
        ...response.data,
        status: getJobStatus(response.data.opening_date, response.data.closing_date)
      };
      setJobs(prev => [...prev, jobWithStatus]);
      setNewJob({
        title: '',
        description: '',
        requirements: '',
        location: '',
        salary_range: '',
        opening_date: '',
        closing_date: ''
      });
      setShowForm(false);
      // Refresh stats
      fetchJobs();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error-message">Error loading dashboard: {error}</div>;

  return (
    <div className="hr-dashboard">
      <div className="dashboard-header">
        <h1>HR Dashboard</h1>
        <button 
          className="create-job-button"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Create New Job'}
        </button>
      </div>

      <div className="stats-overview">
        <div className="stat-card">
          <h3>Total Jobs</h3>
          <p className="stat-number">{stats.totalJobs}</p>
        </div>
        <div className="stat-card">
          <h3>Active Jobs</h3>
          <p className="stat-number">{stats.activeJobs}</p>
        </div>
        <div className="stat-card">
          <h3>Upcoming Jobs</h3>
          <p className="stat-number">{stats.upcomingJobs}</p>
        </div>
        <div className="stat-card">
          <h3>Total Applications</h3>
          <p className="stat-number">{stats.totalApplications}</p>
        </div>
      </div>

      {showForm && (
        <div className="create-job-form">
          <h2>Create New Job Posting</h2>
          <form onSubmit={handleCreateJob}>
            <div className="form-group">
              <label htmlFor="title">Job Title</label>
              <input
                type="text"
                id="title"
                name="title"
                value={newJob.title}
                onChange={handleInputChange}
                required
                placeholder="e.g., Senior Software Engineer"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={newJob.description}
                onChange={handleInputChange}
                required
                placeholder="Detailed job description..."
                rows="4"
              />
            </div>

            <div className="form-group">
              <label htmlFor="requirements">Requirements</label>
              <textarea
                id="requirements"
                name="requirements"
                value={newJob.requirements}
                onChange={handleInputChange}
                required
                placeholder="Required skills and qualifications..."
                rows="3"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="location">Location</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={newJob.location}
                  onChange={handleInputChange}
                  required
                  placeholder="e.g., Kuala Lumpur"
                />
              </div>

              <div className="form-group">
                <label htmlFor="salary_range">Salary Range</label>
                <input
                  type="text"
                  id="salary_range"
                  name="salary_range"
                  value={newJob.salary_range}
                  onChange={handleInputChange}
                  required
                  placeholder="e.g., RM 8000 - RM 12000"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="opening_date">Opening Date</label>
                <input
                  type="date"
                  id="opening_date"
                  name="opening_date"
                  value={newJob.opening_date}
                  onChange={handleInputChange}
                  required
                  min={new Date().toISOString().split('T')[0]}
                />
              </div>

              <div className="form-group">
                <label htmlFor="closing_date">Closing Date</label>
                <input
                  type="date"
                  id="closing_date"
                  name="closing_date"
                  value={newJob.closing_date}
                  onChange={handleInputChange}
                  required
                  min={newJob.opening_date || new Date().toISOString().split('T')[0]}
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="submit-button">Create Job</button>
              <button 
                type="button" 
                className="cancel-button"
                onClick={() => setShowForm(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="jobs-section">
        <h2>Existing Job Postings</h2>
        <div className="jobs-grid">
          {jobs.map((job) => (
            <div key={job.id} className="job-card">
              <div className="job-card-header">
                <h3>{job.title}</h3>
                <span className={`job-status ${job.status}`}>
                  {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                </span>
              </div>

              <div className="job-details">
                <p className="job-location">
                  <i className="location-icon">📍</i> {job.location}
                </p>
                <p className="job-salary">
                  <i className="salary-icon">💰</i> {job.salary_range}
                </p>
              </div>

              <div className="job-dates">
                <p className="opening-date">
                  <i className="calendar-icon">📅</i> Opens: {formatDate(job.opening_date)}
                </p>
                <p className="closing-date">
                  <i className="calendar-icon">⏰</i> Closes: {formatDate(job.closing_date)}
                </p>
              </div>

              <p className="job-description">
                {job.description.length > 100 
                  ? `${job.description.substring(0, 100)}...` 
                  : job.description}
              </p>

              <div className="job-requirements">
                <h4>Requirements:</h4>
                <p>{job.requirements.length > 80 
                  ? `${job.requirements.substring(0, 80)}...` 
                  : job.requirements}</p>
              </div>

              <div className="job-actions">
                <Link to={`/dashboard/${job.id}`} className="dashboard-button">
                  View Dashboard
                </Link>
                {job.status === 'open' && (
                  <Link to={`/apply/${job.id}`} className="apply-link">
                    Candidate Apply Link
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HRDashboard; 