from app.rag.pdf_loader import PDFLoader
from app.rag.text_cleaner import TextCleaner
from app.rag.chunker import Chunker

loader = PDFLoader("data/benefits_docs")

documents = loader.load_documents()

cleaner = TextCleaner()
documents = cleaner.clean(documents)

chunker = Chunker()
chunks = chunker.chunk(documents)

print("=" * 80)

print("Total Chunks:", len(chunks))

print()

print(chunks[0].metadata)

print()

print(chunks[0].content)