from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.config import settings


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


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
