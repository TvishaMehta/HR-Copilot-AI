from pydantic import BaseModel

class ResumeRequest(BaseModel):
    name: str
    email: str
    resume_text: str