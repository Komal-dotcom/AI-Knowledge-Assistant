from backend.app.services.llm_service import (
    LLMService,
)
from backend.app.services.retrieval_service import (
    RetrievalService,
)


class RAGService:

    def __init__(self) -> None:

        self.retrieval_service = (
            RetrievalService()
        )

        self.llm_service = (
            LLMService()
        )

    def ask(
        self,
        question: str,
    ) -> str:

        results = (
            self.retrieval_service.retrieve(
                question
            )
        )

        context = "\n\n".join(
            result.text
            for result in results
        )

        return self.llm_service.generate_answer(
            question=question,
            context=context,
        )