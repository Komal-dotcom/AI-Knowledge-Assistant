from backend.app.services.retrieval_service import RetrievalService

service = RetrievalService()

query = input("Question: ")

results = service.retrieve(query)

print("\nRESULTS\n")

for index, result in enumerate(results, start=1):

    print("=" * 80)

    print(f"Result {index}")

    print(f"Document: {result.filename}")

    print(f"Page: {result.page_number}")

    print(f"Similarity: {result.similarity_score:.4f}")

    print()

    print(result.text[:500])

    print()