"""
Source Discovery Orchestrator.
Manages registered permitted sources and fetches items with strict rate controls,
preventing indiscriminate scraping and preserving provenance.
"""

import logging
from typing import List, Dict, Any
from .base import BaseSource
from .public_curated import CuratedPublicFeedSource
from ..intelligence.pipeline import IngestionItem

logger = logging.getLogger(__name__)


class SourceDiscoveryService:
    """Discovers and polls permitted sources."""

    def __init__(self):
        self._registered_sources: Dict[str, BaseSource] = {}
        # Register default curated public feed
        default_feed = CuratedPublicFeedSource()
        self.register_source(default_feed)

    def register_source(self, source: BaseSource):
        """Registers a permitted source adapter."""
        self._registered_sources[source.source_name] = source
        logger.info(f"Registered source: {source.source_name}")

    def discover_and_fetch(self, source_names: List[str] = None, limit_per_source: int = 20) -> List[IngestionItem]:
        """Polls registered sources and gathers items for pipeline processing."""
        collected: List[IngestionItem] = []
        target_sources = source_names or list(self._registered_sources.keys())

        for name in target_sources:
            src = self._registered_sources.get(name)
            if not src:
                logger.warning(f"Requested source '{name}' is not registered.")
                continue

            try:
                items = src.fetch_items(limit=limit_per_source)
                collected.extend(items)
                logger.info(f"Fetched {len(items)} items from source '{name}'")
            except Exception as e:
                logger.error(f"Error fetching from source '{name}': {e}")

        return collected
