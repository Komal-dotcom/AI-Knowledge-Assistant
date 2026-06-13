from backend.app.services.embedding_service import EmbeddingService

service = EmbeddingService()

vector = service.generate_embedding(
    "Hello World"
)

print(type(vector))
print(len(vector))