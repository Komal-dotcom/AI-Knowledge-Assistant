import chromadb

client = chromadb.PersistentClient(
    path="vector_db"
)

collections = client.list_collections()

print(collections)