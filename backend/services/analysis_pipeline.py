import json
import numpy as np

from backend.services.embedding_service import embedding_service
from backend.services.llm_service import llm


class AnalysisPipeline:

    def cosine_similarity(self, a, b):
        """
        Basic cosine similarity using normalized embeddings
        (your embeddings are already normalized, so dot product works)
        """
        return float(np.dot(a, b))


    def run(self, resume_text: str, job_description: str):

        # -----------------------------
        # 1. EMBEDDINGS
        # -----------------------------
        resume_emb = embedding_service.get_embedding(resume_text)
        jd_emb = embedding_service.get_embedding(job_description)


        # -----------------------------
        # 2. BASIC SIMILARITY SIGNAL
        # -----------------------------
        similarity = self.cosine_similarity(resume_emb, jd_emb)
        similarity_score = round(similarity * 100, 2)


        # -----------------------------
        # 3. LLM REASONING LAYER
        # -----------------------------
        prompt = f"""
You are an ATS (Applicant Tracking System) evaluator.

You are given a semantic similarity score computed from embeddings.

Use it as a strong signal, but not the only factor.

Semantic Similarity Score: {similarity_score}

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY valid JSON in this format:

{{
    "match_percentage": 0,
    "matching_skills": [],
    "missing_skills": [],
    "recommendation": ""
}}

Rules:
- match_percentage must be between 0 and 100
- matching_skills must come from resume
- missing_skills must come from JD gaps
- recommendation must be one of:
  "Strong Match", "Moderate Match", "Weak Match"
- output must be STRICT JSON only
"""

        response = llm.run(prompt)

        # clean LLM output
        response = response.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(response)
        except Exception:
            # fallback safety
            result = {
                "match_percentage": int(similarity_score),
                "matching_skills": [],
                "missing_skills": [],
                "recommendation": "Moderate Match"
            }

        return result


# singleton instance (IMPORTANT for reuse)
analysis_pipeline = AnalysisPipeline()