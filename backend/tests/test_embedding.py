from app.rag.providers.gemini_embeddings import GeminiEmbeddingProvider

provider = GeminiEmbeddingProvider()

vector = provider.embed(
    "Dental plans cover orthodontic treatment."
)

print(type(vector))
print(len(vector))
print(vector[:10])