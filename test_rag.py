from backend.app.services.rag_service import RAGService

service = RAGService()

question = input("Question: ")

answer = service.ask(question)

print("\nANSWER\n")
print(answer)