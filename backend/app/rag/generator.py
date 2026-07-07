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

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply:

"I couldn't find that information in the provided benefits documents."

Be concise and accurate.

-------------------------
Context
-------------------------

{context}

-------------------------
Question
-------------------------

{question}

-------------------------
Answer
-------------------------
"""

        response = self.llm.invoke(prompt)

        return response.content