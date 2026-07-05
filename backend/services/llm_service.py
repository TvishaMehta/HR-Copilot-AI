from groq import Groq
from backend.core.config import settings
import json
import time
import asyncio

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def run(self, prompt: str):
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert HR analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    def run_json(self, prompt: str, retries: int = 2):
        """
        Safe JSON execution with retry logic.
        """

        for attempt in range(retries):
            response = self.run(prompt)

            cleaned = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            try:
                return json.loads(cleaned)

            except json.JSONDecodeError:
                print(f"[LLM Retry] Attempt {attempt + 1} failed...")
                time.sleep(0.5)

        return {
            "match_percentage": 0,
            "strengths": [],
            "missing_skills": [],
            "recommendation": "Hold",
            "interview_questions": []
        }

    async def arun_json(self, prompt: str, retries: int = 2):
        """
        Async wrapper around run_json().
        Executes the blocking Groq call in a worker thread.
        """
        return await asyncio.to_thread(
            self.run_json,
            prompt,
            retries
        )