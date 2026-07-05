from fastapi import APIRouter

from backend.schemas.jd_search import JDSearchRequest
from backend.services.jd_search_service import search_candidates

router = APIRouter()


@router.post("/jd/search")
async def jd_search(req: JDSearchRequest):
    print("[JD SEARCH HIT] request:", req.job_description)

    results = await search_candidates(req.job_description)

    print("[JD SEARCH RESULT COUNT]:", len(results))

    print("[CANDIDATE IDS]:", [r["candidate_id"] for r in results])

    return {
        "matches": results
    }