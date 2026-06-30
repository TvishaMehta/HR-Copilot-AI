from fastapi import FastAPI
from backend.api.routes import (
    health,
    hello,
    jd_match,
    resume_router
)

app = FastAPI(title="HR Copilot AI Backend")


@app.get("/")
def home():
    return {
        "message": "HR Copilot Backend Running"
    }

app.include_router(health.router)
app.include_router(hello.router)
app.include_router(jd_match.router)
app.include_router(resume_router.router)