from pydantic import BaseModel
from typing import List
from backend.schemas.candidate_score import CandidateScore


class ResumeAnalysis(BaseModel):
    skills: List[str]
    experience_summary: str
    suitable_roles: List[str]
    strengths: List[str]
    weaknesses: List[str]
    score: CandidateScore


class ResumeResponse(BaseModel):
    candidate: str
    analysis: ResumeAnalysis