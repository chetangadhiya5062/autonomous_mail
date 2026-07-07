from qdrant_client import QdrantClient

from app.core.config import settings
from app.rag.config import QDRANT_COLLECTION

client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
)

collections = [c.name for c in client.get_collections().collections]

if QDRANT_COLLECTION in collections:
    client.delete_collection(QDRANT_COLLECTION)
    print("Collection deleted.")

else:
    print("Collection does not exist.")