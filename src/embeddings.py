from sentence_transformers import SentenceTransformer

from src.config.settings import settings


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
        )
        return vectors.tolist()