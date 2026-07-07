from app.rag.rag_service import RAGService

rag = RAGService()

question = input("Question: ")

answer = rag.ask(question)

print("\n")
print("=" * 80)
print(answer)
print("=" * 80)