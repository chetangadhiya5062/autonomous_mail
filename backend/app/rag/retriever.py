from typing import List

from qdrant_client import QdrantClient

from app.core.config import settings
from app.rag.config import TOP_K, QDRANT_COLLECTION
from app.rag.document import Document
# from app.rag.providers.sentence_transformer_embeddings import (
#     SentenceTransformerEmbeddingProvider,
# )
from app.rag.providers.factory import get_embedding_provider

class Retriever:

    def __init__(self):

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        # self.embedding_provider = SentenceTransformerEmbeddingProvider()
        self.embedding_provider = get_embedding_provider()

    def search(
        self,
        query: str,
        top_k: int = TOP_K,
    ) -> List[Document]:

        query_vector = self.embedding_provider.embed(query)

        # hits = self.client.search(
        #     collection_name=QDRANT_COLLECTION,
        #     query_vector=query_vector,
        #     limit=top_k,
        # )

        response = self.client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=query_vector,
            limit=top_k,
        )

        hits = response.points

        documents = []

        for hit in hits:

            payload = hit.payload

            metadata = dict(payload)

            content = metadata.pop("content")

            metadata["score"] = hit.score

            documents.append(
                Document(
                    content=content,
                    metadata=metadata,
                )
            )

        return documents