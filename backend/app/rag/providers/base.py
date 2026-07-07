from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingProvider(ABC):
    """
    Base interface for all embedding providers.
    """

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Returns embedding dimension.
        """
        pass

    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> List[float]:
        """
        Embed one text.
        """
        pass

    @abstractmethod
    def embed_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Embed multiple texts.
        """
        pass