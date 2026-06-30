print("\n######## USING THIS resume.py ########\n")

print(__file__)

print("\n******** LOADING backend/services/resume_service.py ********\n")

from backend.services.llm_service import LLMService
import json

llm = LLMService()


def analyze_resume(data):

    print("\n******** analyze_resume() CALLED ********\n")
    print("Candidate:", data.name)
    print("EXPECTING NESTED SCORE OBJECT")

    prompt = f"""
Analyze the resume below.

Return ONLY valid JSON.

Format:

{{
    "skills": [],
    "experience_summary": "",
    "suitable_roles": [],
    "strengths": [],
    "weaknesses": [],
    "score": {{
        "technical_score": 0,
        "project_score": 0,
        "experience_score": 0,
        "communication_score": 0,
        "overall_score": 0
    }}
}}

Resume:

{data.resume_text}

Rules:
- skills should be a list of strings.
- suitable_roles should be a list of strings.
- strengths should be a list of strings.
- weaknesses should be a list of strings.
- technical_score should evaluate technical knowledge and skills.
- project_score should evaluate project quality and complexity.
- experience_score should evaluate experience level and relevance.
- communication_score should evaluate communication and leadership qualities.
- overall_score should summarize the candidate profile.
- All scores must be integers between 0 and 100.
- Return JSON only.
"""

    print("\n******** SENDING PROMPT TO GROQ ********\n")

    response = llm.run(prompt)
    response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    print("\n================ RAW RESPONSE ================\n")
    print(response)
    print("\n==============================================\n")

    try:
        analysis = json.loads(response)
        print("\n******** JSON PARSE SUCCESSFUL ********\n")

    except Exception as e:

        print("\n******** JSON PARSE FAILED ********")
        print(e)

        analysis = {
            "raw_response": response
        }

    print("\n******** RETURNING RESPONSE ********\n")

    return {
        "candidate": data.name,
        "analysis": analysis
    }


def analyze_resume_text(name: str, email: str, resume_text: str):

    class ResumeData:
        pass

    data = ResumeData()
    data.name = name
    data.email = email
    data.resume_text = resume_text

    return analyze_resume(data)