from typing import List

from qdrant_client.models import PointStruct

from app.rag.document import Document
from app.rag.providers.gemini_embeddings import GeminiEmbeddingProvider


class Embedder:

    def __init__(self):

        self.embedding_provider = GeminiEmbeddingProvider()

    def embed_document(
        self,
        document: Document,
    ) -> PointStruct:
        """
        Convert one Document into one Qdrant PointStruct.
        """

        vector = self.embedding_provider.embed(document.content)

        return PointStruct(
            id=document.chunk_id,
            vector=vector,
            payload={
                "content": document.content,
                **document.metadata,
            },
        )

    def embed_documents(
        self,
        documents: List[Document],
    ) -> List[PointStruct]:
        """
        Convert many Documents into Qdrant PointStructs.
        """

        if not documents:
            return []

        print(f"Embedding {len(documents)} documents...")

        texts = [doc.content for doc in documents]

        vectors = self.embedding_provider.embed_batch(texts)

        points = []

        for document, vector in zip(documents, vectors):

            points.append(
                PointStruct(
                    id=document.chunk_id,
                    vector=vector,
                    payload={
                        "content": document.content,
                        **document.metadata,
                    },
                )
            )

        return points