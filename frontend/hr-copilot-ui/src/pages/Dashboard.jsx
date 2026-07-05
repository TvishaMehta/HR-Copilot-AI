import { useState } from "react";
import JobDescriptionForm from "../components/JobDescriptionForm";
import CandidateCard from "../components/CandidateCard";
import CandidateDrawer from "../components/CandidateDrawer";
import { searchCandidates } from "../api/client";

import "../dashboard.css";

export default function Dashboard() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [selectedForCompare, setSelectedForCompare] = useState([]);
  const [compareMode, setCompareMode] = useState(false);

  async function handleSearch(jobDescription) {
    setLoading(true);

    try {
      const data = await searchCandidates(jobDescription);
      setResults(data.matches || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  const topScore =
    results.length > 0
      ? Math.round(
          Math.max(...results.map((c) => c.analysis?.match_percentage || 0))
        )
      : 0;

  const averageScore =
    results.length > 0
      ? Math.round(
          results.reduce(
            (sum, c) => sum + (c.analysis?.match_percentage || 0),
            0
          ) / results.length
        )
      : 0;

  return (
    <div className="dashboard-container">
      <header className="hero">
        <h1>HR Copilot AI</h1>
        <p>AI-Powered Recruitment Assistant</p>
      </header>

      <section className="search-box">
        <JobDescriptionForm onSearch={handleSearch} />
      </section>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing resumes...</p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <>
          <section className="summary-grid">
            <div className="summary-card">
              <h2>{results.length}</h2>
              <span>Candidates</span>
            </div>

            <div className="summary-card">
              <h2>{averageScore}%</h2>
              <span>Average Match</span>
            </div>

            <div className="summary-card">
              <h2>{topScore}%</h2>
              <span>Top Match</span>
            </div>
          </section>

          <div className="results-header">
            <h2>Top Candidates</h2>
          </div>

          <div className="compare-bar">

          <button
            onClick={() => setCompareMode(!compareMode)}
          >
            {compareMode ? "Exit Compare Mode" : "Compare Candidates"}
          </button>

          {compareMode && (
            <span>
              Selected: {selectedForCompare.length}
            </span>
          )}

          </div>

          <div className="results-grid">
            {results.map((candidate, index) => (
              <CandidateCard
                key={candidate.candidate_id}
                candidate={candidate}
                rank={index + 1}
                onClick={() => {
                  if (compareMode) {
                    setSelectedForCompare((prev) => {
                      const exists = prev.find(
                        (c) => c.candidate_id === candidate.candidate_id
                      );

                      if (exists) {
                        return prev.filter(
                          (c) => c.candidate_id !== candidate.candidate_id
                        );
                      }

                      return [...prev, candidate];
                    });
                  } else {
                    setSelectedCandidate(candidate);
                  }
                }}
              />
            ))}
          </div>
        </>
      )}

      {selectedForCompare.length >= 2 && (
  <div className="compare-panel">

    <h2>Candidate Comparison</h2>

    <div className="compare-grid">

      {selectedForCompare.map((c) => (
        <div key={c.candidate_id} className="compare-card">

          <h3>{c.candidate_name}</h3>

          <p>{c.analysis?.recommendation}</p>

          <h4>{c.analysis?.match_percentage}%</h4>

          <div>
            <strong>Skills</strong>
            <ul>
              {c.analysis?.matching_skills?.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

          <div>
            <strong>Missing</strong>
            <ul>
              {c.analysis?.missing_skills?.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

        </div>
      ))}

    </div>

  </div>
)}

      {selectedCandidate && (
        <CandidateDrawer
          candidate={selectedCandidate}
          onClose={() => setSelectedCandidate(null)}
        />
      )}
    </div>
  );
}