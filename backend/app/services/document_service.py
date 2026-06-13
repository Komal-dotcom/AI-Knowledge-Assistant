from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile

from backend.app.config import Settings, settings
from backend.app.core.exceptions import DocumentNotFoundError, DocumentValidationError
from backend.app.core.security import (
    read_upload_with_size_limit,
    sanitize_filename,
    validate_pdf_content_type,
    validate_pdf_filename,
)


@dataclass
class SavedDocument:
    document_id: str
    filename: str
    size_bytes: int
    file_path: Path
    uploaded_at: datetime


class DocumentService:
    def __init__(self, app_settings: Settings | None = None) -> None:
        self._settings = app_settings or settings

    async def upload_document(self, file: UploadFile) -> SavedDocument:
        if file.filename is None:
            raise DocumentValidationError("No file was provided.")

        safe_filename = sanitize_filename(file.filename)
        validate_pdf_filename(safe_filename)
        validate_pdf_content_type(file.content_type)

        content, size_bytes = await read_upload_with_size_limit(
            file,
            self._settings.max_upload_size_bytes,
        )

        document_id = str(uuid4())
        document_dir = self._settings.upload_dir / document_id
        document_dir.mkdir(parents=True, exist_ok=True)

        file_path = document_dir / safe_filename
        file_path.write_bytes(content)

        return SavedDocument(
            document_id=document_id,
            filename=safe_filename,
            size_bytes=size_bytes,
            file_path=file_path,
            uploaded_at=datetime.now(UTC),
        )

    def get_document_by_id(self, document_id: str) -> SavedDocument:
        try:
            UUID(document_id)
        except ValueError as exc:
            raise DocumentNotFoundError("Document not found.") from exc

        document_dir = self._settings.upload_dir / document_id
        if not document_dir.is_dir():
            raise DocumentNotFoundError("Document not found.")

        pdf_files = sorted(document_dir.glob("*.pdf"))
        if not pdf_files:
            raise DocumentNotFoundError("Document not found.")

        file_path = pdf_files[0]
        stat = file_path.stat()

        return SavedDocument(
            document_id=document_id,
            filename=file_path.name,
            size_bytes=stat.st_size,
            file_path=file_path,
            uploaded_at=datetime.fromtimestamp(stat.st_ctime, tz=UTC),
        )
