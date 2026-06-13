from backend.app.models.domain import ChunkedDocument
from backend.app.pipeline.text_chunker import chunk_document
from backend.app.services.extraction_service import ExtractionService


class ChunkingService:

    def __init__(
        self,
        extraction_service: ExtractionService | None = None,
    ) -> None:

        self._extraction_service = (
            extraction_service
            or ExtractionService()
        )

    def chunk_document(
        self,
        document_id: str,
    ) -> ChunkedDocument:

        extracted = self._extraction_service.extract_document(
            document_id
        )

        return chunk_document(extracted)