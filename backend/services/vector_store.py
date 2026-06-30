import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)  # cosine similarity (if normalized)
        self.vectors = []
        self.metadata = []

    def add(self, vector: np.ndarray, metadata: dict):
        vector = np.array(vector).astype("float32").reshape(1, -1)
        self.index.add(vector)
        self.vectors.append(vector)
        self.metadata.append(metadata)

    def search(self, query_vector: np.ndarray, k: int = 3):
        query_vector = np.array(query_vector).astype("float32").reshape(1, -1)
        scores, indices = self.index.search(query_vector, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                results.append({
                    "score": float(score),
                    "data": self.metadata[idx]
                })

        return results