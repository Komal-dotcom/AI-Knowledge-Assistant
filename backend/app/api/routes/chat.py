from fastapi import APIRouter

from backend.app.models.schemas import (
    QuestionRequest,
    QuestionResponse,
)
from backend.app.services.rag_service import (
    RAGService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

rag_service = RAGService()


@router.post(
    "/ask",
    response_model=QuestionResponse,
)
async def ask_question(
    request: QuestionRequest,
) -> QuestionResponse:

    answer = rag_service.ask(
        request.question
    )

    return QuestionResponse(
        answer=answer
    )