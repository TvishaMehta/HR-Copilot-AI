from pydantic import BaseModel
from typing import List


class JDMatchRequest(BaseModel):
    resume_text: str
    job_description: str


class JDMatchResponse(BaseModel):
    match_percentage: int
    matching_skills: List[str]
    missing_skills: List[str]
    recommendation: str