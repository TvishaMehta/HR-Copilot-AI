from backend.services.bm25_service import BM25Service


class BM25GlobalStore:
    def __init__(self):
        self.store = {}  # candidate_id → BM25Service

    def index_candidate(self, candidate_id, chunks):
        bm25 = BM25Service()
        bm25.index(chunks)
        self.store[candidate_id] = bm25

    def search_all(self, query, k=10):
        results = []

        for candidate_id, bm25 in self.store.items():
            res = bm25.search(query, k=k)

            for r in res:
                r["data"]["metadata"]["candidate_id"] = candidate_id
                results.append(r)

        return results


bm25_global = BM25GlobalStore()