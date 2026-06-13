import asyncio

from backend.app.config import Settings, settings
from backend.app.models.domain import ExtractedDocument
from backend.app.pipeline.pdf_extractor import extract_text_from_pdf
from backend.app.services.document_service import DocumentService


class ExtractionService:
    def __init__(
        self,
        document_service: DocumentService | None = None,
        app_settings: Settings | None = None,
    ) -> None:
        self._settings = app_settings or settings
        self._document_service = document_service or DocumentService(self._settings)

    def extract_document(self, document_id: str) -> ExtractedDocument:
        document = self._document_service.get_document_by_id(document_id)

        return extract_text_from_pdf(
            document.file_path,
            document_id=document.document_id,
            filename=document.filename,
        )

    async def extract_document_async(self, document_id: str) -> ExtractedDocument:
        return await asyncio.to_thread(self.extract_document, document_id)
