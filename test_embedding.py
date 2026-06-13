from backend.app.services.embedding_service import EmbeddingService

service = EmbeddingService()

embedding = service.generate_embedding(
    "Machine learning is amazing"
)

print(type(embedding))
print(len(embedding))