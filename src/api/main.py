from fastapi import FastAPI
from pydantic import BaseModel

from src.generation.generator import Generator


app = FastAPI()

generator = Generator(top_k=3)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def read_root():
    return {"message": "VectorDNA API is running"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = generator.answer(request.question)

    sources = [
        {
            "source": item["source"],
            "section": item["section"],
            "score": item["score"],
        }
        for item in result["results"]
    ]

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": sources,
    }