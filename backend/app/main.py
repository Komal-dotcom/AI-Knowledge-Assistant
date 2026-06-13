from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.api.routes.documents import router as documents_router
from backend.app.config import settings
from backend.app.core.exceptions import (
    DocumentNotFoundError,
    DocumentValidationError,
    PdfExtractionError,
)
from backend.app.api.routes.chat import (
    router as chat_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.vector_db_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title=settings.app_name,
    description="RAG-based document question answering system.",
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.debug,
)

app.include_router(documents_router)
app.include_router(chat_router)

@app.exception_handler(DocumentValidationError)
async def document_validation_exception_handler(
    _request: Request,
    exc: DocumentValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.exception_handler(DocumentNotFoundError)
async def document_not_found_exception_handler(
    _request: Request,
    exc: DocumentNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.exception_handler(PdfExtractionError)
async def pdf_extraction_exception_handler(
    _request: Request,
    exc: PdfExtractionError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
