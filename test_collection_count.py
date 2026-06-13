import chromadb

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_collection(
    "documents"
)

print(
    collection.count()
)