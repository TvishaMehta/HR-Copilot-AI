from fastapi import APIRouter
from backend.schemas.jd_match import JDMatchRequest
from backend.services.embedding_service import embedding_service
from backend.services.vector_store_instance import vector_store

router = APIRouter()


@router.post("/jd/match")
def jd_match(data: JDMatchRequest):

    # 1. JD → embedding
    job_emb = embedding_service.get_embedding(data.job_description)

    # 2. FAISS search
    results = vector_store.search(job_emb, k=5)

    # 3. Format into Option B structure
    top_matches = []

    for item in results:
        top_matches.append({
            "score": float(item["score"]),
            "resume_text": item["data"].get("resume_text"),
            "metadata": {
                k: v for k, v in item["data"].items()
                if k != "resume_text"
            }
        })

    return {
        "top_matches": top_matches
    }