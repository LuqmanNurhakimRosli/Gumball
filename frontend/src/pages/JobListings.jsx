import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getJobs } from '../api/api';

function JobListings() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLocation, setFilterLocation] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await getJobs();
      setJobs(response.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         job.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLocation = !filterLocation || job.location.toLowerCase().includes(filterLocation.toLowerCase());
    return matchesSearch && matchesLocation;
  });

  if (loading) return <div className="loading">Loading jobs...</div>;
  if (error) return <div className="error-message">Error loading jobs: {error}</div>;

  return (
    <div className="job-listings">
      <div className="job-listings-header">
        <h1>Available Positions</h1>
        <div className="search-filters">
          <input
            type="text"
            placeholder="Search jobs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <input
            type="text"
            placeholder="Filter by location..."
            value={filterLocation}
            onChange={(e) => setFilterLocation(e.target.value)}
            className="location-input"
          />
        </div>
      </div>

      <div className="jobs-grid">
        {filteredJobs.map((job) => (
          <div key={job.id} className="job-card">
            <div className="job-card-header">
              <h2>{job.title}</h2>
              <span className={`job-status ${job.status.toLowerCase()}`}>
                {job.status}
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

            <p className="job-description">
              {job.description.length > 150 
                ? `${job.description.substring(0, 150)}...` 
                : job.description}
            </p>

            <div className="job-requirements">
              <h3>Requirements:</h3>
              <p>{job.requirements.length > 100 
                ? `${job.requirements.substring(0, 100)}...` 
                : job.requirements}</p>
            </div>

            <div className="job-actions">
              <Link to={`/apply/${job.id}`} className="apply-button">
                Apply Now
              </Link>
              <Link to={`/dashboard/${job.id}`} className="details-button">
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>

      {filteredJobs.length === 0 && (
        <div className="no-jobs">
          <p>No jobs found matching your criteria.</p>
        </div>
      )}
    </div>
  );
}

export default JobListings; 