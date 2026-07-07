from app.rag.context_builder import ContextBuilder
from app.rag.generator import Generator
from app.rag.retriever import Retriever

question = "What dental services are covered?"

retriever = Retriever()
documents = retriever.search(question)

builder = ContextBuilder()
context = builder.build(documents)

generator = Generator()

answer = generator.generate(
    question=question,
    context=context,
)

print("\n" + "=" * 80)
print(answer)
print("=" * 80)