from typing import List

from sentence_transformers import SentenceTransformer

from app.rag.providers.base import BaseEmbeddingProvider


# class SentenceTransformerEmbeddingProvider(BaseEmbeddingProvider):
#     """
#     Local embedding provider using Sentence Transformers.
#     """

#     def __init__(self):

#         self.model = SentenceTransformer(
#             "BAAI/bge-small-en-v1.5"
#         )

#Load the model only once and reuse it for all instances of the class
class SentenceTransformerEmbeddingProvider(BaseEmbeddingProvider):

    _model = None

    def __init__(self):
        if SentenceTransformerEmbeddingProvider._model is None:
            SentenceTransformerEmbeddingProvider._model = SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )

        self.model = SentenceTransformerEmbeddingProvider._model
        
    @property
    def dimension(self) -> int:
        # return self.model.get_sentence_embedding_dimension()
        return self.model.get_embedding_dimension()
    
    def embed(
        self,
        text: str,
    ) -> List[float]:

        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return vectors.tolist()