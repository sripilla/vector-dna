import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

from fastapi import FastAPI, HTTPException

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from src.generation.generator import Generator

logger = logging.getLogger(__name__)

app = FastAPI(
    title="VectorDNA API",
    description="A local RAG API for answering Python questions using documentation.",
    version="1.0.0",
)

generator = Generator(top_k=3)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty or whitespace")

        return value

class Source(BaseModel):
    source: str
    section: str
    score: float


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]


@app.get(
    "/",
    tags=["System"],
    summary="API status",
    description="Returns a basic message confirming that the VectorDNA API is running.",
)
def read_root():
    return {"message": "VectorDNA API is running"}


@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
    description="Returns the current health status of the VectorDNA API.",
)
def health_check():
    return {
        "status": "healthy",
        "service": "VectorDNA API",
    }

@app.post(
    "/ask",
    response_model=AnswerResponse,
    tags=["RAG"],
    summary="Ask a Python question",
    description="Retrieves relevant Python documentation and generates a grounded answer using the local language model.",
)
def ask_question(request: QuestionRequest):
    start_time = time.perf_counter()
    logger.info("Received question: %s", request.question)

    try:
        result = generator.answer(request.question)
    except Exception:
        logger.exception("Failed to generate answer")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer",
        )

    sources = [
        {
            "source": item["source"],
            "section": item["section"],
            "score": item["score"],
        }
        for item in result["results"]
    ]

    logger.info(
    "Generated answer with %d sources",
    len(sources),
)
    elapsed = time.perf_counter() - start_time

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": sources,
    }