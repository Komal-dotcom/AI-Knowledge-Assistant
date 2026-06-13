from backend.app.services.indexing_service import IndexingService

service = IndexingService()

document_id = input("Document ID: ")

service.index_document(document_id)

print("Document indexed successfully!")