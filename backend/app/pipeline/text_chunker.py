from uuid import uuid4

from backend.app.models.domain import (
    ChunkedDocument,
    DocumentChunk,
    ExtractedDocument,
)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_document(
    document: ExtractedDocument,
) -> ChunkedDocument:

    chunks = []

    for page in document.pages:

        text = page.text

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end]

            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    document_id=document.document_id,
                    filename=document.filename,
                    page_number=page.page_number,
                    text=chunk_text,
                    char_count=len(chunk_text),
                )
            )

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return ChunkedDocument(
        document_id=document.document_id,
        filename=document.filename,
        chunks=chunks,
    )