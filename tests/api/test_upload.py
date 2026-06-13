from pathlib import Path

import pytest

from tests.helpers import MINIMAL_PDF


@pytest.mark.asyncio
async def test_upload_document_success(client, upload_dir):
    response = await client.post(
        "/upload-document",
        files={"file": ("sample.pdf", MINIMAL_PDF, "application/pdf")},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["filename"] == "sample.pdf"
    assert data["size_bytes"] == len(MINIMAL_PDF)
    assert data["message"] == "Document uploaded successfully."
    assert "document_id" in data
    assert "uploaded_at" in data

    saved_files = list(Path(upload_dir).glob("*/*.pdf"))
    assert len(saved_files) == 1
    assert saved_files[0].read_bytes() == MINIMAL_PDF


@pytest.mark.asyncio
async def test_upload_document_rejects_non_pdf(client, upload_dir):
    response = await client.post(
        "/upload-document",
        files={"file": ("notes.txt", b"plain text", "text/plain")},
    )

    assert response.status_code == 400
    assert "Only PDF files" in response.json()["detail"]
    assert list(Path(upload_dir).glob("*")) == []


@pytest.mark.asyncio
async def test_upload_document_rejects_invalid_pdf_content(client, upload_dir):
    response = await client.post(
        "/upload-document",
        files={"file": ("fake.pdf", b"not-a-pdf", "application/pdf")},
    )

    assert response.status_code == 400
    assert "not a valid PDF" in response.json()["detail"]
    assert list(Path(upload_dir).glob("*")) == []


@pytest.mark.asyncio
async def test_upload_document_rejects_oversized_file(
    client,
    upload_dir,
    small_max_upload,
):
    oversized_pdf = MINIMAL_PDF + b"x" * (small_max_upload + 1)

    response = await client.post(
        "/upload-document",
        files={"file": ("large.pdf", oversized_pdf, "application/pdf")},
    )

    assert response.status_code == 400
    assert "maximum allowed size" in response.json()["detail"]
    assert list(Path(upload_dir).glob("*")) == []
