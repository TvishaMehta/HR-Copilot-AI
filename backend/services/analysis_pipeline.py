import json
import numpy as np

from backend.services.embedding_service import embedding_service
from backend.services.recruiter_service import llm
from backend.services.role_classifier import RoleClassifier


class AnalysisPipeline:

    def __init__(self):
        self.role_classifier = RoleClassifier()

    # -----------------------------
    # cosine similarity
    # -----------------------------
    def cosine_similarity(self, a, b):
        return float(np.dot(a, b))

    # -----------------------------
    # skill extraction
    # -----------------------------
    def extract_skills(self, text):
        skills = [
            "python", "java", "react", "node", "aws",
            "docker", "kubernetes", "tensorflow", "pytorch",
            "sql", "mongodb", "pandas", "numpy", "nlp",
            "machine learning", "deep learning",
            "rest api", "express", "typescript"
        ]

        text = text.lower()
        return set(s for s in skills if s in text)

    # -----------------------------
    # skill overlap score
    # -----------------------------
    def skill_score(self, resume, jd):
        r = self.extract_skills(resume)
        j = self.extract_skills(jd)

        if not j:
            return 0.0

        return len(r.intersection(j)) / len(j)

    # -----------------------------
    # normalization (prevents collapse)
    # -----------------------------
    def normalize(self, x, min_v=0.30, max_v=0.95):
        return max(min(x, max_v), min_v)

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------
    def run(self, resume_text: str, job_description: str):

        # 1. ROLE CLASSIFICATION
        resume_role = self.role_classifier.classify(resume_text)
        jd_role = self.role_classifier.classify(job_description)

        role_match = 1.0 if resume_role == jd_role else 0.65

        # 2. EMBEDDINGS
        resume_emb = embedding_service.get_embedding(resume_text)
        jd_emb = embedding_service.get_embedding(job_description)

        semantic = self.cosine_similarity(resume_emb, jd_emb)
        semantic = self.normalize(semantic)

        # 3. SKILL SCORE
        skill = self.skill_score(resume_text, job_description)

        # 4. FINAL SCORE (CORE FIX)
        base_score = (
            0.60 * semantic +
            0.30 * skill +
            0.10 * role_match
        )

        # role penalty (prevents DevOps = Full Stack issue)
        if resume_role != jd_role:
            base_score *= 0.75

        base_score = round(base_score * 100, 2)

        # 5. LLM ONLY EXPLANATION
        prompt = f"""
You are an ATS evaluator.

Do NOT compute score.
Only explain results.

Score: {base_score}

Resume:
{resume_text}

Job Description:
{job_description}

Return JSON ONLY:

{{
  "matching_skills": [],
  "missing_skills": [],
  "recommendation": "",
  "reasoning": ""
}}
"""

        response = llm.run(prompt)
        response = response.replace("```json", "").replace("```", "").strip()

        try:
            explanation = json.loads(response)
        except:
            explanation = {
                "matching_skills": [],
                "missing_skills": [],
                "recommendation": "Moderate Match",
                "reasoning": "LLM parsing failed"
            }

        return {
            "match_percentage": base_score,
            "role": {
                "resume_role": resume_role,
                "jd_role": jd_role
            },
            "signals": {
                "semantic_score": round(semantic * 100, 2),
                "skill_score": round(skill * 100, 2),
                "role_match": role_match
            },
            **explanation
        }


analysis_pipeline = AnalysisPipeline()