from qdrant_client import QdrantClient

from src.config.settings import settings


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=settings.qdrant_url,
    )


def main() -> None:
    client = get_qdrant_client()

    collections = client.get_collections()

    print("✓ Connected to Qdrant")
    print(f"Collections: {collections.collections}")


if __name__ == "__main__":
    main()