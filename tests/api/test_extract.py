from pathlib import Path

import pytest

from tests.helpers import create_sample_pdf


@pytest.mark.asyncio
async def test_extract_document_returns_structured_pages(client, upload_dir):
    pdf_bytes = create_sample_pdf(["Alpha content", "Beta content"])

    upload_response = await client.post(
        "/upload-document",
        files={"file": ("notes.pdf", pdf_bytes, "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = await client.get(f"/document/{document_id}/extract")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["document_id"] == document_id
    assert data["filename"] == "notes.pdf"
    assert data["total_pages"] == 2
    assert len(data["pages"]) == 2
    assert data["pages"][0]["page_number"] == 1
    assert data["pages"][1]["page_number"] == 2
    assert "Alpha content" in data["pages"][0]["text"]
    assert "Beta content" in data["pages"][1]["text"]
    assert "[Page 1]" in data["full_text"]
    assert "[Page 2]" in data["full_text"]


@pytest.mark.asyncio
async def test_extract_document_returns_404_for_unknown_id(client, upload_dir):
    response = await client.get(
        "/document/00000000-0000-0000-0000-000000000000/extract",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."
