from backend.app.services.chunking_service import ChunkingService

service = ChunkingService()

document_id = input("Document ID: ")

chunked = service.chunk_document(document_id)

print(f"\nTotal Chunks: {len(chunked.chunks)}")

print("\nFirst Chunk:\n")
print(chunked.chunks[0].text[:500])