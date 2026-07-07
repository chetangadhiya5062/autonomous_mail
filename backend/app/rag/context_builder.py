from typing import List

from app.rag.document import Document


class ContextBuilder:
    """
    Builds the textual context supplied to the LLM.
    """

    def build(
        self,
        documents: List[Document],
    ) -> str:

        sections = []

        for index, document in enumerate(documents, start=1):

            metadata = document.metadata

            section = f"""
Document {index}
Source : {metadata.get("document")}
Page   : {metadata.get("page")}
Score  : {metadata.get("score", 0):.4f}

Content:
{document.content}
"""

            sections.append(section.strip())

        return "\n\n" + ("\n\n" + "=" * 80 + "\n\n").join(sections)