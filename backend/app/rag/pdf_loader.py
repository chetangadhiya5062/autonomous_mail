from pathlib import Path
from app.rag.document import Document
import fitz


class PDFLoader:
    """
    Loads PDFs and extracts text page-by-page.
    """

    def __init__(self, pdf_directory: str):
        self.pdf_directory = Path(pdf_directory)

    def load_documents(self):
        """
        Returns a list of pages from all PDFs.

        Each page is represented as a dictionary:
        {
            document_name,
            page_number,
            text
        }
        """

        documents = []

        pdf_files = sorted(self.pdf_directory.glob("*.pdf"))

        print(f"\nFound {len(pdf_files)} PDF(s).\n")

        for pdf_path in pdf_files:

            print(f"Reading: {pdf_path.name}")

            pdf = fitz.open(pdf_path)

            for page_index in range(len(pdf)):

                page = pdf.load_page(page_index)

                text = page.get_text("text")

                if not text.strip():
                    continue

                documents.append(
                    Document(
                        content=text,
                        metadata={
                            "document": pdf_path.name,
                            "page": page_index + 1,
                        }
                    )
                )

            pdf.close()

        print(f"\nLoaded {len(documents)} pages.\n")

        return documents