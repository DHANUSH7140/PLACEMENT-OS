"""
Question Text & Code Normalizer.
Canonicalizes raw question texts, strips artifacts, standardizes whitespace and punctuation,
and generates deterministic SHA-256 hashes for exact deduplication.
"""

import re
import hashlib
from typing import Tuple


class QuestionNormalizer:
    """Provides consistent text normalization and hashing across all ingestion channels."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalizes a string for canonical comparison:
        - Replaces typographic quotes/dashes with ASCII
        - Collapses repeated whitespace, newlines, and tabs
        - Lowercases tokens
        - Strips extraneous trailing/leading symbols
        """
        if not text:
            return ""

        # Normalize unicode quotes and dashes
        s = text.strip()
        s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        s = s.replace("–", "-").replace("—", "-").replace("…", "...")
        
        # Remove markdown bold/italic wrapper symbols for canonical representation
        s = re.sub(r"[*_]{1,3}", "", s)

        # Standardize mathematical symbols and operators
        s = s.replace("≤", "<=").replace("≥", ">=").replace("≠", "!=")

        # Strip common boilerplate prompts e.g., "Problem Statement:", "Given that:", etc.
        s = re.sub(r"^(problem statement[:\s]*|description[:\s]*|task[:\s]*|question[:\s]*)", "", s, flags=re.IGNORECASE).strip()

        # Collapse whitespace
        s = re.sub(r"\s+", " ", s).strip()

        return s

    @staticmethod
    def generate_content_hash(text: str) -> str:
        """
        Generates SHA-256 hash of normalized text.
        Guarantees that identical questions from different sources yield the exact same hash.
        """
        normalized = QuestionNormalizer.normalize_text(text).lower()
        # Keep only alphanumeric and basic punctuation for hash stability
        clean = re.sub(r"[^a-z0-9]", "", normalized)
        return hashlib.sha256(clean.encode("utf-8")).hexdigest()

    @staticmethod
    def clean_title(title: str, max_length: int = 120) -> str:
        """Cleans and truncates a question title to readable format."""
        if not title:
            return "Untitled Question"
        t = re.sub(r"\s+", " ", title).strip()
        # Remove leading numbers like "1. ", "Problem 42 - "
        t = re.sub(r"^(\d+[\.\-\)]\s*|problem\s+\d+[:\-\s]*)", "", t, flags=re.IGNORECASE).strip()
        if len(t) > max_length:
            t = t[:max_length].rsplit(" ", 1)[0] + "..."
        return t.title() if t.islower() else t
