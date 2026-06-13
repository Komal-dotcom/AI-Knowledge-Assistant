from backend.app.services.chunking_service import (
    ChunkingService,
)
from backend.app.services.vector_store_service import (
    VectorStoreService,
)


class IndexingService:

    def __init__(self) -> None:

        self.chunking_service = (
            ChunkingService()
        )

        self.vector_store = (
            VectorStoreService()
        )

    def index_document(
        self,
        document_id: str,
    ) -> None:

        chunked_document = (
            self.chunking_service.chunk_document(
                document_id
            )
        )

        for chunk in chunked_document.chunks:

            self.vector_store.add_chunk(
                chunk
            )