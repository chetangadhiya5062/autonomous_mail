from app.rag.qdrant_store import QdrantStore

store = QdrantStore()

store.create_collection()

print("Qdrant connection successful!")