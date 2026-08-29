from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.config import settings


COLLECTION_NAME = "python_docs"


def setup_collection():
    client = QdrantClient(url=f"http://{settings.qdrant_url}")

    collections = client.get_collections().collections

    if COLLECTION_NAME not in [c.name for c in collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )
        print(f"✓ Created collection: {COLLECTION_NAME}")
    else:
        print(f"✓ Collection already exists: {COLLECTION_NAME}")


if __name__ == "__main__":
    setup_collection()