from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.rag_service import RAGService

router = APIRouter()

rag = RAGService()


class Source(BaseModel):
    document: str
    page: int


class BenefitsRequest(BaseModel):
    question: str


class BenefitsResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[Source]


@router.post(
    "/ask",
    response_model=BenefitsResponse,
)
def ask_question(
    payload: BenefitsRequest,
):

    response = rag.ask(payload.question)

    return BenefitsResponse(
        answer=response.answer,
        confidence=response.confidence,
        sources=response.sources,
    )