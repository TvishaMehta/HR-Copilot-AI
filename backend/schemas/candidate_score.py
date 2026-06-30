from pydantic import BaseModel


class CandidateScore(BaseModel):
    technical_score: int
    project_score: int
    experience_score: int
    communication_score: int
    overall_score: int