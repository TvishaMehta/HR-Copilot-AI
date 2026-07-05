from fastapi import APIRouter
from backend.services.embedding_service import embedding_service
from backend.services.vector_store_instance import vector_store
from backend.schemas.resume import ResumeRequest
from backend.services.resume_chunker import resume_chunker

router = APIRouter()


@router.post("/add_resume")
def add_resume(data: ResumeRequest):
    print("🔥 ADD_RESUME FILE LOADED:", __file__)

    candidate_id = data.email.lower().strip()

    chunks = resume_chunker.chunk_resume(data.resume_text)

    for chunk in chunks:

        chunk["metadata"].update({
            "candidate_id": candidate_id,
            "candidate_name": data.name,
            "email": data.email
        })

        embedding = embedding_service.get_embedding(chunk["text"])

        vector_store.add(
            embedding,
            chunk
        )

    print("Vectors in FAISS:", len(vector_store.metadata))

    return {
        "message": "Resume added successfully.",
        "candidate_id": candidate_id,
        "chunks_stored": len(chunks)
    }