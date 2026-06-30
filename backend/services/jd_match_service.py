from backend.services.llm_service import LLMService
import json

llm = LLMService()


def match_resume_with_jd(resume_text: str, job_description: str):

    prompt = f"""
You are an ATS system.

Compare the resume and the job description.

Return ONLY valid JSON.

Format:

{{
    "match_percentage": 0,
    "matching_skills": [],
    "missing_skills": [],
    "recommendation": ""
}}

Resume:

{resume_text}

Job Description:

{job_description}

Rules:
- match_percentage must be an integer between 0 and 100.
- matching_skills must be a list.
- missing_skills must be a list.
- recommendation should be one of:
    Strong Match
    Moderate Match
    Weak Match

Return JSON only.
"""

    response = llm.run(prompt)

    response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(response)