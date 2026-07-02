from backend.app.config import settings
from backend.app.services.document_service import DocumentService
from backend.app.services.extraction_service import ExtractionService
from backend.app.services.indexing_service import IndexingService
from backend.app.services.vector_store_service import VectorStoreService

def get_document_service() -> DocumentService:
    return DocumentService(app_settings=settings)


def get_extraction_service() -> ExtractionService:
    return ExtractionService(
        document_service=get_document_service(),
        app_settings=settings,
    )
def get_indexing_service() -> IndexingService:
    return IndexingService()

def get_vector_store_service() -> VectorStoreService:
    return VectorStoreService()