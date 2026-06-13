from fastapi import APIRouter, Depends, File, UploadFile, status

from backend.app.api.dependencies import get_document_service, get_extraction_service
from backend.app.models.schemas import ExtractDocumentResponse, UploadDocumentResponse
from backend.app.services.document_service import DocumentService
from backend.app.services.extraction_service import ExtractionService

router = APIRouter(tags=["Documents"])


@router.post(
    "/upload-document",
    response_model=UploadDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a PDF document",
)
async def upload_document(
    file: UploadFile = File(..., description="PDF file to upload"),
    document_service: DocumentService = Depends(get_document_service),
) -> UploadDocumentResponse:
    saved = await document_service.upload_document(file)

    return UploadDocumentResponse(
        status="success",
        document_id=saved.document_id,
        filename=saved.filename,
        size_bytes=saved.size_bytes,
        uploaded_at=saved.uploaded_at,
        message="Document uploaded successfully.",
    )


@router.get(
    "/document/{document_id}/extract",
    response_model=ExtractDocumentResponse,
    summary="Extract text from an uploaded PDF",
)
async def extract_document_text(
    document_id: str,
    extraction_service: ExtractionService = Depends(get_extraction_service),
) -> ExtractDocumentResponse:
    extracted = await extraction_service.extract_document_async(document_id)

    return ExtractDocumentResponse(
        status="success",
        document_id=extracted.document_id,
        filename=extracted.filename,
        total_pages=extracted.total_pages,
        pages=[
            {
                "page_number": page.page_number,
                "text": page.text,
                "char_count": page.char_count,
            }
            for page in extracted.pages
        ],
        full_text=extracted.full_text,
        message="Text extracted successfully.",
    )
