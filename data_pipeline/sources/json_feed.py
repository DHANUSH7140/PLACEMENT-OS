"""
JSON and Webhook Ingestion Adapter.
Parses structured JSON payloads received via APIs, webhook triggers, or export files.
"""

import json
from typing import List, Dict, Any
from .base import BaseSource
from ..intelligence.pipeline import IngestionItem


class JsonFeedSource(BaseSource):
    """Parses JSON streams or file dumps of questions."""

    def __init__(self, feed_data: List[Dict[str, Any]], source_name: str = "json_feed"):
        super().__init__(source_name=source_name)
        self.feed_data = feed_data

    @classmethod
    def from_file(cls, file_path: str, source_name: str = "json_file_feed") -> "JsonFeedSource":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "questions" in data:
                data = data["questions"]
        return cls(feed_data=data, source_name=source_name)

    def fetch_items(self, limit: int = 50) -> List[IngestionItem]:
        items = []
        for idx, entry in enumerate(self.feed_data[:limit]):
            raw_text = entry.get("problem_statement") or entry.get("raw_text") or entry.get("text") or ""
            if not raw_text:
                continue

            items.append(
                IngestionItem(
                    raw_text=raw_text,
                    title=entry.get("title", ""),
                    source_name=entry.get("source_name", self.source_name),
                    source_url=entry.get("source_url"),
                    source_item_id=entry.get("source_item_id", f"json_{idx}"),
                    category=entry.get("category"),
                    subcategory=entry.get("subcategory"),
                    topic=entry.get("topic"),
                    difficulty=entry.get("difficulty"),
                    companies=entry.get("companies", []),
                    roles=entry.get("roles", []),
                    question_type=entry.get("question_type", "Coding"),
                    options=entry.get("options"),
                    correct_answer=entry.get("correct_answer"),
                    observed_frequency=entry.get("observed_frequency", 1),
                )
            )
        return items
