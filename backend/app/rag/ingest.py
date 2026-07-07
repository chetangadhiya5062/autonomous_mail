from qdrant_client.models import PointStruct

from app.rag.pdf_loader import PDFLoader
from app.rag.text_cleaner import TextCleaner
from app.rag.chunker import Chunker
from app.rag.embedder import Embedder
from app.rag.qdrant_store import QdrantStore
from app.rag.config import UPLOAD_BATCH_SIZE


PDF_DIRECTORY = "data/benefits_docs"


def batch(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def main():

    print("\n========== AetherMail RAG Ingestion ==========\n")

    # --------------------------------------------------
    # Load PDFs
    # --------------------------------------------------

    loader = PDFLoader(PDF_DIRECTORY)

    documents = loader.load_documents()

    # --------------------------------------------------
    # Clean text
    # --------------------------------------------------

    cleaner = TextCleaner()

    documents = cleaner.clean(documents)

    # --------------------------------------------------
    # Chunk
    # --------------------------------------------------

    chunker = Chunker()

    chunks = chunker.chunk(documents)

    print(f"Total Chunks : {len(chunks)}")

    # --------------------------------------------------
    # Qdrant
    # --------------------------------------------------

    store = QdrantStore()

    store.create_collection()

    # --------------------------------------------------
    # Embedder
    # --------------------------------------------------

    embedder = Embedder()

    total_batches = (len(chunks) + UPLOAD_BATCH_SIZE - 1) // UPLOAD_BATCH_SIZE

    START_BATCH = 20  # Change this when resuming

    for batch_number, chunk_batch in enumerate(
        batch(chunks, UPLOAD_BATCH_SIZE),
        start=1,
    ):

        if batch_number < START_BATCH:
            continue

        print(
            f"\nBatch {batch_number}/{total_batches}"
        )

        points = embedder.embed_documents(chunk_batch)

        store.insert_many(points)

    print("\n========== INGESTION COMPLETE ==========\n")


if __name__ == "__main__":
    main()