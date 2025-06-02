import React, { useState } from 'react';
import axios from 'axios'; // Import axios for direct file upload (or use the api.js pattern)
import { API_URL } from '../api/api'; // Assuming API_URL is exported from api.js

function ResumeAnalyzerPage() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [requirements, setRequirements] = useState(''); // New state for requirements
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFiles(Array.from(event.target.files));
    setAnalysisResults(null); // Clear previous results
    setError(null); // Clear previous errors
  };

  const handleRequirementsChange = (event) => {
    setRequirements(event.target.value);
    setAnalysisResults(null); // Clear results when requirements change
    setError(null);
  };

  const handleAnalyze = async () => {
    if (selectedFiles.length === 0) {
      setError('Please select at least one file.');
      return;
    }
    if (!requirements.trim()) {
        setError('Please enter job requirements.');
        return;
    }

    setLoading(true);
    setError(null);
    setAnalysisResults(null);

    const formData = new FormData();
    formData.append('requirements', requirements); // Append requirements
    selectedFiles.forEach(file => {
      formData.append('files', file); // 'files' is the key expected by the backend endpoint
    });

    try {
      // Use axios directly for FormData upload or create a specific api.js function
      const response = await axios.post(`${API_URL}/ai/analyze-resumes`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAnalysisResults(response.data);
    } catch (err) {
      console.error('Error analyzing resumes:', err.response?.data || err.message);
      setError(err.response?.data?.detail || 'Failed to analyze resumes.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-analyzer-page">
      <h1>Resume AI Analyzer</h1>
      <p>Upload multiple resumes (PDF or DOCX) and provide job requirements to get AI analysis and ranking.</p>

      <div className="requirements-input-section form-group">
         <label htmlFor="requirements">Job Requirements (e.g., React.js, Python, 3+ years experience)</label>
         <textarea
            id="requirements"
            value={requirements}
            onChange={handleRequirementsChange}
            rows="3"
            placeholder="Enter comma-separated job requirements here..."
            required
         />
      </div>

      <div className="file-input-section">
        <input
          type="file"
          multiple
          accept=".pdf,.doc,.docx"
          onChange={handleFileChange}
        />
        <button onClick={handleAnalyze} disabled={selectedFiles.length === 0 || !requirements.trim() || loading}>
          {loading ? 'Analyzing...' : 'Analyze Resumes'}
        </button>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}

      {analysisResults && (
        <div className="analysis-results">
          <h2>Analysis Results (Ranked by Score)</h2>
          {analysisResults.length === 0 ? (
            <p>No valid resumes were analyzed.</p>
          ) : (
            <ul className="ranked-list">
              {analysisResults.map((result, index) => (
                <li key={index} className={`result-item status-${result.status ? result.status.toLowerCase().replace(/\s+/g, '-') : 'failed'}`}>
                  <h3>{index + 1}. {result.filename}</h3>
                  {result.score !== null ? (
                    <>
                      <p>AI Score: <strong>{result.score !== undefined ? result.score.toFixed(2) : 'N/A'}</strong></p>
                      <p>Status: <strong>{result.status || 'N/A'}</strong></p>
                      <p>Analysis: {result.analysis || 'No analysis provided.'}</p>
                    </>
                  ) : (
                    <p>Status: <strong>{result.status || 'Failed'}</strong></p>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default ResumeAnalyzerPage; 