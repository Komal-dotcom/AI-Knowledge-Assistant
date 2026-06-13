from io import BytesIO
from pathlib import Path

import fitz

MINIMAL_PDF = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF"


def create_sample_pdf(
    pages: list[str],
    output_path: Path | None = None,
) -> bytes:
    """Build a multi-page PDF with known text for tests."""
    document = fitz.open()

    try:
        for page_text in pages:
            page = document.new_page()
            page.insert_text((72, 72), page_text)

        if output_path is not None:
            document.save(output_path)
            return output_path.read_bytes()

        buffer = BytesIO()
        document.save(buffer)
        return buffer.getvalue()
    finally:
        document.close()
