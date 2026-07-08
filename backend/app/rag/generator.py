# backend/app/rag/generator.py

from app.agent.llm import get_llm


class Generator:

    def __init__(self):

        self.llm = get_llm()

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are AetherMail's Benefits Assistant.

Your responsibility is to answer employee benefit questions
ONLY using the information provided in the Context.

Rules:

1. Never use outside knowledge.

2. Never guess or infer information that is not explicitly stated.

3. If the Context does not contain the answer, respond exactly with:

I couldn't find that information in the provided benefits documents.

4. Keep answers concise and professional.

5. Use bullet points whenever the answer contains multiple benefits,
coverage items or conditions.

6. Do not mention the Context or retrieved documents unless the user
explicitly asks.

=========================
Context
=========================

{context}

=========================
Question
=========================

{question}

=========================
Answer
=========================
"""
        # response = self.llm.invoke(prompt)
        response = self.llm.invoke(
            prompt.strip()
        )

        return response.content