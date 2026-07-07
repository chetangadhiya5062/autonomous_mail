from app.rag.providers.sentence_transformer_embeddings import (
    SentenceTransformerEmbeddingProvider,
)

provider = SentenceTransformerEmbeddingProvider()

print(provider.dimension)