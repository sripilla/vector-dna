from pathlib import Path

from src.corpus.chunker import chunk_sections
from src.corpus.parser import parse_document


CORPUS_ROOT = Path("data/raw/python-3.14-docs-text")


def build_corpus() -> list[dict]:
    chunks = []

    files = sorted(CORPUS_ROOT.rglob("*.txt"))

    for path in files:
        sections = parse_document(path)

        document_chunks = chunk_sections(
            sections,
            source=str(path.relative_to(CORPUS_ROOT)),
        )

        chunks.extend(document_chunks)

    return chunks


if __name__ == "__main__":
    chunks = build_corpus()

    print(f"Documents: {len(list(CORPUS_ROOT.rglob('*.txt')))}")
    print(f"Chunks: {len(chunks)}")