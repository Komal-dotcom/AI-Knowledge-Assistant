from fastapi import APIRouter, Depends, File, UploadFile, status

from backend.app.api.dependencies import (
    get_document_service,
    get_extraction_service,
    get_indexing_service,
)
from backend.app.api.dependencies import get_vector_store_service
from backend.app.models.schemas import DeleteDocumentResponse
from backend.app.services.vector_store_service import VectorStoreService

from backend.app.services.indexing_service import IndexingService
from backend.app.models.schemas import (
    ExtractDocumentResponse,
    UploadDocumentResponse,
    DocumentSummaryResponse,
    ListDocumentsResponse,
)
from backend.app.services.document_service import DocumentService
from backend.app.services.extraction_service import ExtractionService

router = APIRouter(tags=["Documents"])


@router.post(
    "/documents",
    response_model=UploadDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a PDF document",
    description="Uploads a PDF, automatically extracts text, generates embeddings, indexes it into ChromaDB, and makes it immediately available for question answering.",
)
async def upload_document(
    file: UploadFile = File(..., description="PDF file to upload"),
    document_service: DocumentService = Depends(get_document_service),
    indexing_service: IndexingService = Depends(get_indexing_service),
) -> UploadDocumentResponse:
    saved = await document_service.upload_document(file)
    indexing_service.index_document(saved.document_id)

    return UploadDocumentResponse(
        status="success",
        document_id=saved.document_id,
        filename=saved.filename,
        size_bytes=saved.size_bytes,
        uploaded_at=saved.uploaded_at,
        ready_for_questions=True,
        message="Document uploaded and indexed successfully.",
    )


@router.get(
    "/document/{document_id}/extract",
    response_model=ExtractDocumentResponse,
    summary="Extract text from a PDF",
    description="Extracts cleaned text from every page of an uploaded PDF document.",
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

@router.get(
    "/documents",
    response_model=ListDocumentsResponse,
    summary="List uploaded documents",
    description="Returns all uploaded PDF documents ordered by upload time (newest first).",
)
async def list_documents(
    document_service: DocumentService = Depends(get_document_service),
) -> ListDocumentsResponse:

    documents = document_service.list_documents()

    return ListDocumentsResponse(
        documents=[
            DocumentSummaryResponse(
                document_id=document.document_id,
                filename=document.filename,
                size_bytes=document.size_bytes,
                uploaded_at=document.uploaded_at,
            )
            for document in documents
        ]
    )
@router.delete(
    "/documents/{document_id}",
    response_model=DeleteDocumentResponse,
    summary="Delete a document",
    description="Deletes the uploaded PDF and removes all associated embeddings from ChromaDB.",
)
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service),
) -> DeleteDocumentResponse:

    vector_store_service.delete_document(document_id)

    document_service.delete_document(document_id)

    return DeleteDocumentResponse(
        status="success",
        message="Document deleted successfully.",
    )