from app.rag.providers.sentence_transformer_embeddings import (
    SentenceTransformerEmbeddingProvider,
)

provider = SentenceTransformerEmbeddingProvider()

vector = provider.embed(
    "Dental insurance covers orthodontic treatment."
)

print(type(vector))
print(len(vector))
print(vector[:10])