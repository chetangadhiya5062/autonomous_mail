# from typing import List

# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# from app.core.config import settings
# from app.rag.providers.base import BaseEmbeddingProvider


# class GeminiEmbeddingProvider(BaseEmbeddingProvider):

#     def __init__(self):

#         self.embeddings = GoogleGenerativeAIEmbeddings(
#             # model="models/text-embedding-004",
#             # model="models/gemini-embedding-001",
#             model=settings.EMBEDDING_MODEL,
#             google_api_key=settings.GEMINI_API_KEY,
#         )

#     def embed(self, text: str) -> List[float]:

#         return self.embeddings.embed_query(text)

# -------------------------------------------above one is of normal embedding-------------------------------------
from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings
from app.rag.providers.base import BaseEmbeddingProvider


class GeminiEmbeddingProvider(BaseEmbeddingProvider):

    def __init__(self):

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )

    def embed(self, text: str) -> List[float]:
        """
        Embed a single document.
        """
        return self.embeddings.embed_query(text)

    def embed_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Embed multiple documents in one API call.
        """
        return self.embeddings.embed_documents(texts)