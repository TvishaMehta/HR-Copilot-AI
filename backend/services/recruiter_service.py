from backend.services.llm_service import LLMService

llm = LLMService()

async def generate_recruiter_report(candidate: dict, job_description: str):
    """
    Generates structured AI-based recruiter analysis for a candidate.
    Uses semantic chunks + LLM evaluation.
    """

    # -----------------------------
    # 1. Build resume context
    # -----------------------------
    resume_context = ""

    for chunk in candidate.get("chunks", []):
        resume_context += (
            f"Section: {chunk.get('section', '')}\n"
            f"Content:\n{chunk.get('text', '')}\n"
            f"{'-' * 40}\n"
        )

    # -----------------------------
    # 2. Prompt for LLM
    # -----------------------------
    prompt = f"""
You are a senior technical recruiter with experience hiring Software Engineers.

You are given:
1. A Job Description
2. Resume sections retrieved using semantic search

Evaluate ONLY using the provided resume information.
Do not invent skills or experience.

Job Description:
{job_description}

Retrieved Resume Information:
{resume_context}

Return ONLY valid JSON:

{{
  "summary": "",
  "match_percentage": 0,
  "experience_level": "",
  "matching_skills": [],
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "recommendation": "",
  "confidence": "",
  "interview_questions": []
}}

Rules:
- summary max 40 words
- match_percentage: 0–100
- experience_level: Junior | Mid-Level | Senior
- recommendation: Proceed | Hold | Reject
- confidence: High | Medium | Low
- interview_questions: exactly 3 items
"""

    # -----------------------------
    # 3. Call LLM (already returns dict)
    # -----------------------------
    response = await llm.arun_json(prompt)

    print("LLM RESPONSE DEBUG:", response)
    print("TYPE:", type(response))

    # -----------------------------
    # 4. Safety check (never crash system)
    # -----------------------------
    if not isinstance(response, dict):
        return {
            "summary": "Invalid LLM response",
            "match_percentage": 0,
            "experience_level": "Unknown",
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "recommendation": "Hold",
            "confidence": "Low",
            "interview_questions": []
        }

    # -----------------------------
    # 5. Ensure required keys exist
    # -----------------------------
    response.setdefault("summary", "")
    response.setdefault("match_percentage", 0)
    response.setdefault("experience_level", "Unknown")
    response.setdefault("matching_skills", [])
    response.setdefault("missing_skills", [])
    response.setdefault("strengths", [])
    response.setdefault("weaknesses", [])
    response.setdefault("recommendation", "Hold")
    response.setdefault("confidence", "Low")
    response.setdefault("interview_questions", [])

    return response