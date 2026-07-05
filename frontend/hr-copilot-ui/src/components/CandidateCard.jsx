export default function CandidateCard({ candidate, rank, onClick }) {
  const analysis = candidate.analysis || {};
  const score = analysis.match_percentage || 0;

  const getBadge = () => {
    if (score >= 85) return "badge-high";
    if (score >= 65) return "badge-mid";
    return "badge-low";
  };

  return (
    <div className="candidate-card" onClick={onClick}>

      <div className="card-top">

        <div className="rank-badge">#{rank}</div>

        <div className="card-main">

          <h3>{candidate.candidate_name}</h3>

          <p className="email">{candidate.email}</p>

          <div className="mini-skills">
            {analysis.matching_skills?.slice(0, 3).map((s, i) => (
              <span key={i} className="mini-skill">
                {s}
              </span>
            ))}
          </div>

        </div>

        <div className={`score-circle ${getBadge()}`}>
          {score}%
        </div>

      </div>

      <div className="card-footer">
        <span className="recommendation-mini">
          {analysis.recommendation || "—"}
        </span>

        <span className="view-hint">
          Click to view details →
        </span>
      </div>

    </div>
  );
}