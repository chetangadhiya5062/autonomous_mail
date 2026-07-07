import re
from typing import List

from app.rag.document import Document


class TextCleaner:
    """
    Cleans extracted PDF text while preserving meaning.
    """

    def clean(self, documents: List[Document]) -> List[Document]:

        cleaned_documents = []

        for doc in documents:

            text = doc.content

            # Normalize line endings
            text = text.replace("\r", "\n")

            # Replace multiple tabs/spaces with one space
            text = re.sub(r"[ \t]+", " ", text)

            # Replace 3+ blank lines with 2
            text = re.sub(r"\n{3,}", "\n\n", text)

            # Strip leading/trailing whitespace
            text = text.strip()

            cleaned_documents.append(
                Document(
                    content=text,
                    metadata=doc.metadata
                )
            )

        return cleaned_documents