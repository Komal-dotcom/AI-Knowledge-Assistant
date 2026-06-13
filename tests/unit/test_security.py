import pytest

from backend.app.core.exceptions import DocumentValidationError
from backend.app.core.security import (
    read_upload_with_size_limit,
    sanitize_filename,
    validate_pdf_content_type,
    validate_pdf_filename,
    validate_pdf_magic_bytes,
)
from tests.helpers import MINIMAL_PDF


class FakeUploadFile:
    def __init__(self, content: bytes) -> None:
        self._content = content
        self._offset = 0

    async def read(self, size: int = -1) -> bytes:
        if size == -1:
            chunk = self._content[self._offset :]
            self._offset = len(self._content)
            return chunk

        chunk = self._content[self._offset : self._offset + size]
        self._offset += len(chunk)
        return chunk


def test_sanitize_filename_strips_path_components():
    assert sanitize_filename("../../notes.pdf") == "notes.pdf"


def test_validate_pdf_filename_rejects_non_pdf():
    with pytest.raises(DocumentValidationError, match="Only PDF files"):
        validate_pdf_filename("report.docx")


def test_validate_pdf_content_type_rejects_invalid_type():
    with pytest.raises(DocumentValidationError, match="Invalid content type"):
        validate_pdf_content_type("text/plain")


def test_validate_pdf_magic_bytes_rejects_invalid_content():
    with pytest.raises(DocumentValidationError, match="not a valid PDF"):
        validate_pdf_magic_bytes(b"not a pdf")


@pytest.mark.asyncio
async def test_read_upload_with_size_limit_accepts_valid_pdf():
    content, size = await read_upload_with_size_limit(
        FakeUploadFile(MINIMAL_PDF),
        max_size_bytes=1024,
    )
    assert content == MINIMAL_PDF
    assert size == len(MINIMAL_PDF)


@pytest.mark.asyncio
async def test_read_upload_with_size_limit_rejects_oversized_file():
    oversized = MINIMAL_PDF + b"x" * 2048
    with pytest.raises(DocumentValidationError, match="maximum allowed size"):
        await read_upload_with_size_limit(
            FakeUploadFile(oversized),
            max_size_bytes=1024,
        )
