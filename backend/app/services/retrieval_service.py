from backend.app.models.domain import RetrievalResult
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store_service import VectorStoreService


class RetrievalService:

    def __init__(self) -> None:

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStoreService()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:

        query_embedding = (
            self.embedding_service.generate_embedding(
                query
            )
        )

        results = (
            self.vector_store.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
            )
        )

        retrieval_results = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        ids = results["ids"][0]
        distances = results["distances"][0]

        for doc, meta, chunk_id, distance in zip(
            documents,
            metadatas,
            ids,
            distances,
        ):

            retrieval_results.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    document_id=meta["document_id"],
                    filename=meta["filename"],
                    page_number=meta["page_number"],
                    text=doc,
                    similarity_score=1 - distance,
                )
            )

        return retrieval_results