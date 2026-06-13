import re
from pathlib import Path

from fastapi import UploadFile

from backend.app.core.exceptions import DocumentValidationError

PDF_MAGIC_BYTES = b"%PDF-"
PDF_EXTENSION = ".pdf"
PDF_CONTENT_TYPES = {"application/pdf", "application/x-pdf"}

CHUNK_SIZE = 1024 * 1024


def sanitize_filename(filename: str | None) -> str:
    if not filename or not filename.strip():
        raise DocumentValidationError("Filename is required.")

    name = Path(filename).name.strip()
    if not name or name in {".", ".."}:
        raise DocumentValidationError("Invalid filename.")

    safe_name = re.sub(r"[^\w.\- ]", "_", name).strip()
    if not safe_name:
        raise DocumentValidationError("Invalid filename.")

    return safe_name


def validate_pdf_filename(filename: str) -> None:
    if not filename.lower().endswith(PDF_EXTENSION):
        raise DocumentValidationError("Only PDF files are allowed.")


def validate_pdf_content_type(content_type: str | None) -> None:
    if content_type and content_type.split(";")[0].strip().lower() not in PDF_CONTENT_TYPES:
        raise DocumentValidationError("Invalid content type. Only PDF files are allowed.")


def validate_pdf_magic_bytes(header: bytes) -> None:
    if not header.startswith(PDF_MAGIC_BYTES):
        raise DocumentValidationError("File content is not a valid PDF.")


async def read_upload_with_size_limit(
    file: UploadFile,
    max_size_bytes: int,
) -> tuple[bytes, int]:
    chunks: list[bytes] = []
    total_size = 0

    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break

        total_size += len(chunk)
        if total_size > max_size_bytes:
            max_mb = max_size_bytes // (1024 * 1024)
            raise DocumentValidationError(
                f"File exceeds the maximum allowed size of {max_mb} MB.",
            )

        chunks.append(chunk)

    content = b"".join(chunks)
    if not content:
        raise DocumentValidationError("Uploaded file is empty.")

    validate_pdf_magic_bytes(content[:1024])
    return content, total_size
