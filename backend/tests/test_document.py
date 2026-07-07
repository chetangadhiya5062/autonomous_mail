from app.rag.document import Document

doc = Document(
    content="Hello",
    metadata={
        "document": "DentalPPO.pdf",
        "page": 10,
        "chunk_index": 2,
    },
)

print(doc.chunk_id)