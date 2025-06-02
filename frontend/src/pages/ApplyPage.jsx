import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getJob, applyForJob } from '../api/api';

function ApplyPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    resume_file: null
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchJobDetails();
  }, [jobId]);

  const fetchJobDetails = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getJob(jobId);
      if (response.data) {
        setJob(response.data);
      } else {
        setError('Job data is empty or invalid.');
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching job details:', err);
      setError(err.response?.data?.detail || 'Job not found or has been removed');
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({
      ...prev,
      resume_file: e.target.files[0]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('email', formData.email);
      formDataToSend.append('phone', formData.phone);
      formDataToSend.append('resume', formData.resume_file);

      await applyForJob(jobId, formDataToSend);
      setSuccess(true);
      
      // Reset form - maybe not necessary if navigating away or showing success message
      // setFormData({
      //   name: '',
      //   email: '',
      //   phone: '',
      //   resume_file: null
      // });
    } catch (err) {
      console.error('Error submitting application:', err);
      setError(err.response?.data?.detail || 'Error submitting application');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading job details...</div>;
  }

  if (error && !job) {
    return <div className="error-message">Error: {error}</div>;
  }

  if (success) {
    return (
      <div className="apply-page">
        <div className="success-message">
          <h2>Thank You for Applying!</h2>
          <p>Your application has been submitted successfully.</p>
          <p>We will review your application.</p>
          <p>You can check your application status on the <Link to="/candidate-status">Candidate Status Page</Link>.</p>
          <button onClick={() => navigate('/')}>Return to Home</button>
        </div>
      </div>
    );
  }

  return (
    <div className="apply-page">
      <h1>Apply for {job?.title || 'Job'}</h1>
      {job && (
        <div className="job-details">
          <p><strong>Location:</strong> {job.location}</p>
          <p><strong>Salary Range:</strong> {job.salary_range}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="application-form">
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="phone">Phone Number</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="resume">Resume (PDF or DOCX)</label>
          <input
            type="file"
            id="resume"
            name="resume_file"
            onChange={handleFileChange}
            accept=".pdf,.doc,.docx"
            required
          />
        </div>

        <button type="submit" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit Application'}
        </button>
      </form>
    </div>
  );
}

export default ApplyPage; 