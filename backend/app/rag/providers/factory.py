from app.rag.providers.sentence_transformer_embeddings import (
    SentenceTransformerEmbeddingProvider,
)

_provider = None


def get_embedding_provider():

    global _provider

    if _provider is None:
        _provider = SentenceTransformerEmbeddingProvider()

    return _provider