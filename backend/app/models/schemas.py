from datetime import datetime

from pydantic import BaseModel, Field


class UploadDocumentResponse(BaseModel):
    status: str
    document_id: str
    filename: str
    size_bytes: int
    uploaded_at: datetime
    ready_for_questions: bool
    message: str


class PageTextResponse(BaseModel):
    page_number: int = Field(..., ge=1, description="1-based page number")
    text: str
    char_count: int = Field(..., ge=0)


class ExtractDocumentResponse(BaseModel):
    status: str = Field(..., examples=["success"])
    document_id: str
    filename: str
    total_pages: int = Field(..., ge=0)
    pages: list[PageTextResponse]
    full_text: str
    message: str


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: str

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question",
    )


class QuestionResponse(BaseModel):
    answer: str

class DocumentSummaryResponse(BaseModel):
    document_id: str
    filename: str
    size_bytes: int
    uploaded_at: datetime


class ListDocumentsResponse(BaseModel):
    documents: list[DocumentSummaryResponse]

class DeleteDocumentResponse(BaseModel):
    status: str
    message: str 