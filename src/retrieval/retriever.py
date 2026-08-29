from src.embeddings import Embedder
from src.vectordb.client import get_qdrant_client
from src.vectordb.setup import COLLECTION_NAME

class Retriever:
    def __init__(self, top_k=5, score_threshold=0.5):
        self.embedder = Embedder()
        self.client = get_qdrant_client()
        self.top_k = top_k
        self.score_threshold = score_threshold

    def search(self, query):
        # Convert the question into a vector
        vector = self.embedder.encode([query])[0]

        # Search Qdrant
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=self.top_k,
        ).points

        # Return only sufficiently relevant results
        return [
            {
                "score": result.score,
                "source": result.payload.get("source"),
                "section": result.payload.get("section"),
                "text": result.payload.get("text"),
            }
            for result in results
            if result.score >= self.score_threshold
        ]