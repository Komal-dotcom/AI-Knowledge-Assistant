import chromadb

from backend.app.models.domain import DocumentChunk
from backend.app.services.embedding_service import (
    EmbeddingService,
)


class VectorStoreService:

    def __init__(self) -> None:

        self.client = chromadb.PersistentClient(
            path="vector_db"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="documents"
            )
        )

        self.embedding_service = (
            EmbeddingService()
        )

    def add_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:

        embedding = (
            self.embedding_service.generate_embedding(
                chunk.text
            )
        )

        self.collection.add(
            ids=[chunk.chunk_id],
            embeddings=[embedding],
            documents=[chunk.text],
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "filename": chunk.filename,
                    "page_number": chunk.page_number,
                }
            ],
        )

    def delete_document(
        self,
        document_id: str,
    ) -> None:

        self.collection.delete(
            where={
                "document_id": document_id
            }
        )