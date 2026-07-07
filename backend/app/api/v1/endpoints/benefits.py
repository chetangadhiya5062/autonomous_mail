from fastapi import APIRouter

from pydantic import BaseModel

from app.rag.rag_service import RAGService

router = APIRouter()

rag = RAGService()


class BenefitsRequest(BaseModel):
    question: str


class BenefitsResponse(BaseModel):
    answer: str


@router.post(
    "/ask",
    response_model=BenefitsResponse,
)
def ask_question(
    payload: BenefitsRequest,
):

    answer = rag.ask(
        payload.question
    )

    return BenefitsResponse(
        answer=answer
    )