"""
Central configuration for the RAG pipeline.
"""

# -------------------------------
# PDF Processing
# -------------------------------

CHUNK_SIZE = 900          # characters

CHUNK_OVERLAP = 150       # characters

MIN_CHUNK_SIZE = 250

UPLOAD_BATCH_SIZE = 50
# -------------------------------
# Retrieval
# -------------------------------

TOP_K = 5
MIN_CONFIDENCE = 0.55
# -------------------------------
# Vector Database
# -------------------------------

QDRANT_COLLECTION = "benefits_documents"

# -------------------------------
# Embedding Model
# -------------------------------

EMBEDDING_MODEL = "gemini"