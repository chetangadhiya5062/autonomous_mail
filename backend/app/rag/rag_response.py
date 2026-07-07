from dataclasses import dataclass
from typing import List, Dict


@dataclass
class RAGResponse:

    answer: str

    confidence: float

    sources: List[Dict]