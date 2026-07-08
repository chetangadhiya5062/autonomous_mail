# rag_service.py
from app.rag.retriever import Retriever
from app.rag.config import MIN_CONFIDENCE
from app.rag.context_builder import ContextBuilder
from app.rag.generator import Generator
from app.rag.rag_response import RAGResponse


class RAGService:

    def __init__(self):

        self.retriever = Retriever()
        self.context_builder = ContextBuilder()
        self.generator = Generator()

    def ask(
        self,
        question: str,
    ) -> RAGResponse:

        documents = self.retriever.search(question)

        if not documents:

            return RAGResponse(
                answer="I couldn't find relevant information in the benefits documents.",
                confidence=0.0,
                sources=[],
            )

        context = self.context_builder.build(documents)

        answer = self.generator.generate(
            question=question,
            context=context,
        )

        confidence = max(
            doc.metadata.get("score", 0)
            for doc in documents
        )
        
        if confidence < MIN_CONFIDENCE:

            return RAGResponse(
                answer=(
                    "I couldn't find reliable information "
                    "about your question in the available "
                    "benefits documents."
                ),
                confidence=confidence,
                sources=[],
            )

        sources = []

        seen = set()

        for doc in documents:

            source = (
                doc.metadata.get("document"),
                doc.metadata.get("page"),
            )

            if source not in seen:

                seen.add(source)

                sources.append(
                    {
                        "document": source[0],
                        "page": source[1],
                    }
                )

        return RAGResponse(
            answer=answer,
            confidence=confidence,
            sources=sources,
        )