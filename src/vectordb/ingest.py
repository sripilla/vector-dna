from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from src.config import settings
from src.corpus.build import build_corpus
from src.embeddings import Embedder
from src.vectordb.setup import COLLECTION_NAME


BATCH_SIZE = 64


def ingest():
    print("Building corpus...")
    chunks = build_corpus()
    print(f"Chunks to ingest: {len(chunks)}")

    client = QdrantClient(url=f"http://{settings.qdrant_url}")
    embedder = Embedder()

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]

        texts = [chunk["text"] for chunk in batch]
        vectors = embedder.encode(texts)

        points = []

        for offset, (chunk, vector) in enumerate(zip(batch, vectors)):
            point_id = start + offset

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=chunk,
                )
            )

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

        end = min(start + BATCH_SIZE, len(chunks))
        print(f"Ingested {end}/{len(chunks)}")


if __name__ == "__main__":
    ingest()