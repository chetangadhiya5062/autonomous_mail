from app.rag.providers.gemini_embeddings import GeminiEmbeddingProvider

provider = GeminiEmbeddingProvider()

texts = [
    "Dental insurance covers orthodontics.",
    "Vision insurance covers eye exams.",
    "Medical plans include emergency services."
]

vectors = provider.embed_batch(texts)

print(type(vectors))
print(len(vectors))
print(len(vectors[0]))