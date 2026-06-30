from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        if self.model is None:
            print("Loading embedding model...")
            self.model = SentenceTransformer(self.model_name)

    def get_embedding(self, text: str):
        self.load_model()
        return np.array(
            self.model.encode(text, normalize_embeddings=True),
            dtype=np.float32
        )

embedding_service = EmbeddingService()