from app.rag.context_builder import ContextBuilder
from app.rag.retriever import Retriever

retriever = Retriever()

documents = retriever.search(
    "What dental services are covered?"
)

builder = ContextBuilder()

context = builder.build(documents)

print(context)