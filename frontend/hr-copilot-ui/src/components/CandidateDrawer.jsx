export default function CandidateDrawer({ candidate, onClose }) {
  if (!candidate) return null;

  const analysis = candidate.analysis || {};

  return (
    <>
      <div className="drawer-overlay" onClick={onClose}></div>

      <div className="candidate-drawer">

        <button
          className="close-btn"
          onClick={onClose}
        >
          ✕
        </button>

        <div className="drawer-header">

          <h2>{candidate.candidate_name}</h2>

          <div className="drawer-score">
            {analysis.match_percentage || 0}%
          </div>

        </div>

        <div className="recommendation">

          <span
            className={`recommendation-badge ${(
              analysis.recommendation || ""
            ).toLowerCase()}`}
          >
            {analysis.recommendation}
          </span>

        </div>

        <section className="drawer-section">

          <h3>📝 AI Summary</h3>

          <p>{analysis.summary}</p>

        </section>

        <section className="drawer-section">

          <h3>👨‍💻 Experience Level</h3>

          <p>{analysis.experience_level}</p>

        </section>

        <section className="drawer-section">

          <h3>📈 Confidence</h3>

          <p>{analysis.confidence}</p>

        </section>

        <section className="drawer-section">

          <h3>✅ Matching Skills</h3>

          <div className="skills">

            {analysis.matching_skills?.map((skill, i) => (
              <span
                key={i}
                className="skill-tag"
              >
                {skill}
              </span>
            ))}

          </div>

        </section>

        <section className="drawer-section">

          <h3>❌ Missing Skills</h3>

          <div className="skills">

            {analysis.missing_skills?.map((skill, i) => (
              <span
                key={i}
                className="missing-tag"
              >
                {skill}
              </span>
            ))}

          </div>

        </section>

        <section className="drawer-section">

          <h3>💪 Strengths</h3>

          <ul>

            {analysis.strengths?.map((item, i) => (
              <li key={i}>{item}</li>
            ))}

          </ul>

        </section>

        <section className="drawer-section">

          <h3>⚠️ Weaknesses</h3>

          <ul>

            {analysis.weaknesses?.map((item, i) => (
              <li key={i}>{item}</li>
            ))}

          </ul>

        </section>

        <section className="drawer-section">

          <h3>🎯 Interview Questions</h3>

          <ol>

            {analysis.interview_questions?.map((q, i) => (
              <li key={i}>{q}</li>
            ))}

          </ol>

        </section>

      </div>
    </>
  );
}