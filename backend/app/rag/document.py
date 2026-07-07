from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Document:

    content: str

    metadata: Dict = field(default_factory=dict)