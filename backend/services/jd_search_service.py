import asyncio
from collections import defaultdict

from backend.services.embedding_service import embedding_service
from backend.services.vector_store_instance import vector_store
from backend.services.recruiter_service import generate_recruiter_report
from backend.services.bm25_global import bm25_global
from backend.eval.ranking_evaluator import evaluator
from backend.eval.ground_truth import build_ground_truth

def rrf_score(faiss_results, bm25_results, k=60):

    scores = defaultdict(float)

    def add(results, weight):
        for rank, r in enumerate(results):
            cid = r["data"]["metadata"]["candidate_id"]
            scores[cid] += weight * (1 / (rank + k))

    add(faiss_results, 1.2)   # semantic stronger
    add(bm25_results, 0.8)    # keyword weaker

    return scores


async def search_candidates(job_description: str, k: int = 10):

    # 1. FAISS
    query_emb = embedding_service.get_embedding(job_description)
    faiss_results = vector_store.search(query_emb, k=k)

    # 2. BM25
    bm25_results = bm25_global.search_all(job_description, k=k)

    # 3. GROUP CANDIDATES
    candidates = {}

    def add(results):
        for r in results:
            chunk = r["data"]
            meta = chunk["metadata"]
            cid = meta["candidate_id"]

            if cid not in candidates:
                candidates[cid] = {
                    "candidate_id": cid,
                    "candidate_name": meta.get("candidate_name"),
                    "email": meta.get("email"),
                    "chunks": [],
                    "sections": set()
                }

            candidates[cid]["chunks"].append(chunk)
            candidates[cid]["sections"].add(chunk["section"])

    add(faiss_results)
    add(bm25_results)

    for c in candidates.values():
        c["sections"] = list(c["sections"])

    # 4. LLM ANALYSIS
    tasks = [
        generate_recruiter_report(c, job_description)
        for c in candidates.values()
    ]

    analyses = await asyncio.gather(*tasks)

    for c, a in zip(candidates.values(), analyses):
        c["analysis"] = a

    # 5. RRF RANKING
    fusion = rrf_score(faiss_results, bm25_results)

    ranked = sorted(
        candidates.values(),
        key=lambda c: fusion.get(c["candidate_id"], 0),
        reverse=True
    )

    return ranked

def attach_evaluation(ranked_candidates, job_description):

    # infer role simply (reuse your classifier if needed)
    job_role = "full_stack"  # simplify for now

    ground_truth = build_ground_truth(job_role)

    metrics = evaluator.evaluate(
        ranked_candidates,
        ground_truth,
        k=10
    )

    return {
        "candidates": ranked_candidates,
        "evaluation": metrics
    }