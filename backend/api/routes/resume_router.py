from fastapi import APIRouter
from backend.services.embedding_service import embedding_service
from backend.services.vector_store_instance import vector_store
from backend.schemas.resume import ResumeRequest

router = APIRouter()


@router.post("/add_resume")
def add_resume(data: ResumeRequest):

    text = data.resume_text

    emb = embedding_service.get_embedding(text)

    vector_store.add(
        emb,
        {"resume_text": text}
    )

    return {"message": "resume added"}