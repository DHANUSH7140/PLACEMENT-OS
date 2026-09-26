"""
Abstract Base Source Adapter for Ingestion.
Ensures all sources adhere to controlled discovery, rate limits, and attribution contracts.
"""

from abc import ABC, abstractmethod
from typing import List
from ..intelligence.pipeline import IngestionItem


class BaseSource(ABC):
    """Abstract interface for all question source adapters."""

    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    def fetch_items(self, limit: int = 50) -> List[IngestionItem]:
        """Fetches normalized IngestionItem objects from the source."""
        pass
