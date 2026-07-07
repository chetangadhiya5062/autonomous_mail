from app.rag.document import Document
from app.rag.embedder import Embedder

doc = Document(
    content="Dental plans cover orthodontic treatment.",
    metadata={
        "document": "Dental.pdf",
        "page": 10,
        "chunk_index": 2,
    },
)

embedder = Embedder()

point = embedder.embed_document(doc)

print(type(point))
print(point.id)
print(len(point.vector))
print(point.payload)