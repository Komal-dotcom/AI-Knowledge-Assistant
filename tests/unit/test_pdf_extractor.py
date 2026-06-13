from pathlib import Path

import pytest

from backend.app.core.exceptions import PdfExtractionError
from backend.app.pipeline.pdf_extractor import extract_text_from_pdf
from tests.helpers import create_sample_pdf


def test_extract_text_from_pdf_preserves_page_numbers(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(
        ["Page one content", "Page two content"],
        output_path=pdf_path,
    )

    extracted = extract_text_from_pdf(
        pdf_path,
        document_id="doc-123",
        filename="sample.pdf",
    )

    assert extracted.document_id == "doc-123"
    assert extracted.filename == "sample.pdf"
    assert extracted.total_pages == 2
    assert len(extracted.pages) == 2
    assert extracted.pages[0].page_number == 1
    assert extracted.pages[1].page_number == 2
    assert "Page one content" in extracted.pages[0].text
    assert "Page two content" in extracted.pages[1].text
    assert extracted.pages[0].char_count == len(extracted.pages[0].text)
    assert "[Page 1]" in extracted.full_text
    assert "[Page 2]" in extracted.full_text


def test_extract_text_from_pdf_raises_for_missing_file(tmp_path: Path):
    with pytest.raises(PdfExtractionError, match="PDF file not found"):
        extract_text_from_pdf(
            tmp_path / "missing.pdf",
            document_id="doc-123",
            filename="missing.pdf",
        )


def test_extract_text_from_pdf_raises_for_invalid_pdf(tmp_path: Path):
    invalid_pdf = tmp_path / "invalid.pdf"
    invalid_pdf.write_bytes(b"not-a-real-pdf")

    with pytest.raises(PdfExtractionError, match="Unable to read PDF"):
        extract_text_from_pdf(
            invalid_pdf,
            document_id="doc-123",
            filename="invalid.pdf",
        )
