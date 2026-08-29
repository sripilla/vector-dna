import ollama

from src.retrieval.retriever import Retriever
from src.retrieval.context import build_context


MODEL_NAME = "llama3.2:3b"


class Generator:
    def __init__(self, top_k: int = 3):
        self.retriever = Retriever(top_k=top_k)

    def answer(self, question: str) -> str:
        # 1. Retrieve relevant documents
        results = self.retriever.search(question)

        # 2. Build context from retrieved documents
        context = build_context(results)

        # 3. Create the RAG prompt
        prompt = f"""
You are a helpful assistant answering questions about Python.

Use ONLY the information provided in the context below.

If the answer cannot be found in the context, say:
"I don't know based on the provided documentation."

Context:
{context}

Question:
{question}

Answer:
"""

        # 4. Ask the local LLM
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]


def main() -> None:
    generator = Generator(top_k=3)

    question = "How does the asyncio event loop work?"

    answer = generator.answer(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()