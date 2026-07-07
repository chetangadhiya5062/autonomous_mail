from dataclasses import dataclass, field
from typing import Dict
# import hashlib
import uuid


@dataclass
class Document:

    content: str
    metadata: Dict = field(default_factory=dict)

    # @property
    # def chunk_id(self) -> str:
    #     """
    #     Deterministic unique ID for this chunk.
    #     Same document/page/chunk_index -> same ID.
    #     """

    #     source = self.metadata.get("document", "")
    #     page = self.metadata.get("page", "")
    #     chunk = self.metadata.get("chunk_index", "")

    #     raw = f"{source}:{page}:{chunk}"

    #     return hashlib.sha256(raw.encode("utf-8")).hexdigest()
    
    @property
    def chunk_id(self) -> str:
        """
        Deterministic UUID for each chunk.
        """

        source = self.metadata.get("document", "")
        page = self.metadata.get("page", "")
        chunk = self.metadata.get("chunk_index", "")

        raw = f"{source}:{page}:{chunk}"

        return str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                raw,
            )
        )