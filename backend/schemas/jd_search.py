from pydantic import BaseModel


class JDSearchRequest(BaseModel):
    job_description: str