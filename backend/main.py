from fastapi import FastAPI
from backend.api.routes import (
    health,
    hello,
    jd_match,
    resume_router
)
from backend.api.routes.jd_search import router as jd_search_router
from fastapi.middleware.cors import CORSMiddleware
print("Imported resume router from:", resume_router.__file__)

app = FastAPI(title="HR Copilot AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "HR Copilot Backend Running"
    }

app.include_router(health.router)
app.include_router(hello.router)
app.include_router(jd_match.router)
app.include_router(resume_router.router)
app.include_router(jd_search_router)

from backend.services.vector_store_instance import vector_store

@app.on_event("startup")
def clear_faiss_on_start():
    vector_store.reset()
    print("[FAISS] CLEAN START")
