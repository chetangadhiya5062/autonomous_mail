from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import Filter

from app.core.config import settings
from app.rag.config import (
    TOP_K,
    QDRANT_COLLECTION,
)
from app.rag.providers.gemini_embeddings import GeminiEmbeddingProvider


class Retriever:

    def __init__(self):

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        self.embedding_provider = GeminiEmbeddingProvider()

    def search(
        self,
        query: str,
        top_k: int = TOP_K,
    ):

        vector = self.embedding_provider.embed(query)

        results = self.client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=vector,
            limit=top_k,
            query_filter=None,
        )

        return results