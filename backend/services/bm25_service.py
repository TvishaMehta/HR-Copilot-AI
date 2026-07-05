from rank_bm25 import BM25Okapi
import re


class BM25Service:
    def __init__(self):
        self.corpus = []
        self.metadata = []
        self.bm25 = None

    def _tokenize(self, text: str):
        return re.findall(r"\w+", text.lower())

    def index(self, chunks):
        self.corpus = []
        self.metadata = []

        for chunk in chunks:
            text = chunk["text"]
            self.corpus.append(self._tokenize(text))
            self.metadata.append(chunk)

        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query: str, k: int = 10):
        if not self.bm25:
            return []

        query_tokens = self._tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )[:k]

        results = []
        for idx, score in ranked:
            results.append({
                "score": float(score),
                "data": self.metadata[idx]
            })

        return results