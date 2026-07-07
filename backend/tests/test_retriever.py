from app.rag.retriever import Retriever

retriever = Retriever()

documents = retriever.search(
    "What dental services are covered?"
)

print("\n" + "=" * 80)

for i, document in enumerate(documents, start=1):

    print(f"Result {i}")
    print("-" * 80)

    print("Score      :", document.metadata.get("score"))
    print("Document   :", document.metadata.get("document"))
    print("Page       :", document.metadata.get("page"))
    print("Chunk      :", document.metadata.get("chunk_index"))

    print()

    print(document.content[:600])

    print("\n" + "=" * 80)