from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingProvider(ABC):

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Return embedding vector."""
        pass