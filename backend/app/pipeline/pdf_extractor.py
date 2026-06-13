from pathlib import Path

import fitz

from backend.app.core.exceptions import PdfExtractionError
from backend.app.models.domain import ExtractedDocument, PageContent
from backend.app.pipeline.text_cleaner import clean_text


def extract_text_from_pdf(
    file_path: Path,
    *,
    document_id: str,
    filename: str,
) -> ExtractedDocument:
    """Extract text from a PDF file, preserving 1-based page numbers."""
    if not file_path.is_file():
        raise PdfExtractionError(f"PDF file not found: {file_path}")

    try:
        with fitz.open(file_path) as document:
            pages: list[PageContent] = []

            for page_index in range(document.page_count):
                page = document.load_page(page_index)
                raw_text = page.get_text("text")
                cleaned_text = clean_text(raw_text)

                pages.append(
                    PageContent(
                        page_number=page_index + 1,
                        text=cleaned_text,
                        char_count=len(cleaned_text),
                    )
                )

            return ExtractedDocument(
                document_id=document_id,
                filename=filename,
                total_pages=document.page_count,
                pages=pages,
            )
    except PdfExtractionError:
        raise
    except fitz.FileDataError as exc:
        raise PdfExtractionError("Unable to read PDF file. The file may be corrupted.") from exc
    except Exception as exc:
        raise PdfExtractionError(f"Failed to extract text from PDF: {exc}") from exc
