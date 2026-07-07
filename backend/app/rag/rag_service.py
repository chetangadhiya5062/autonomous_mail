from app.rag.retriever import Retriever
from app.rag.context_builder import ContextBuilder
from app.rag.generator import Generator


class RAGService:

    def __init__(self):

        self.retriever = Retriever()
        self.context_builder = ContextBuilder()
        self.generator = Generator()

    def ask(
        self,
        question: str,
    ) -> str:

        documents = self.retriever.search(question)

        if not documents:
            return "I couldn't find relevant information in the benefits documents."

        context = self.context_builder.build(documents)

        return self.generator.generate(
            question=question,
            context=context,
        )