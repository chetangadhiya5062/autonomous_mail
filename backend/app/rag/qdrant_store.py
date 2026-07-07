from typing import List, Dict, Any
from uuid import UUID

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.core.config import settings
from app.rag.config import QDRANT_COLLECTION


class QdrantStore:

    def __init__(
        self,
        # collection_name: str = "benefits_documents",
        # collection_name: str = settings.QDRANT_COLLECTION,
        collection_name: str = QDRANT_COLLECTION,
        vector_size: int = 3072,
    ):

        self.collection_name = collection_name

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        self.vector_size = vector_size

    def create_collection(self):

        collections = self.client.get_collections().collections

        existing = [c.name for c in collections]

        if self.collection_name in existing:
            print(f"Collection '{self.collection_name}' already exists.")
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

        print(f"Collection '{self.collection_name}' created.")

    def insert(
        self,
        point_id: str,
        vector: List[float],
        payload: Dict[str, Any],
    ):

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )
        

    def insert_many(
        self,
        points: List[PointStruct],
    ):
        
        if not points:
            print("No vectors to insert.")
            return

        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

        print(f"Inserted {len(points)} vectors.")