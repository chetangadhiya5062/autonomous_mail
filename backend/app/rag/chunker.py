from typing import List

from app.rag.document import Document
from app.rag.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MIN_CHUNK_SIZE,
)


class Chunker:
    """
    Splits cleaned documents into overlapping chunks.
    """

    def chunk(self, documents: List[Document]) -> List[Document]:

        chunks = []

        for document in documents:

            text = document.content

            start = 0
            chunk_index = 0

            while start < len(text):

                end = start + CHUNK_SIZE

                chunk_text = text[start:end]

                if len(chunk_text.strip()) < MIN_CHUNK_SIZE:
                    break

                metadata = dict(document.metadata)

                metadata["chunk_index"] = chunk_index

                metadata["start_char"] = start

                metadata["end_char"] = min(end, len(text))

                chunks.append(
                    Document(
                        content=chunk_text,
                        metadata=metadata,
                    )
                )

                chunk_index += 1

                start += CHUNK_SIZE - CHUNK_OVERLAP

        return chunks