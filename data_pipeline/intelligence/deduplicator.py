"""
Question Deduplication Engine.
Performs two tiers of deduplication:
1. Exact content hash deduplication (SHA-256)
2. Semantic / Token-overlap deduplication (Jaccard n-gram and token cosine)
Handles metadata merging according to canonical rules.
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone
from ..models.question import Question, QuestionSource
from .normalizer import QuestionNormalizer


class DeduplicationResult:
    def __init__(self, is_duplicate: bool, canonical_question: Optional[Question] = None, match_type: str = "NONE", similarity_score: float = 0.0):
        self.is_duplicate = is_duplicate
        self.canonical_question = canonical_question
        self.match_type = match_type  # EXACT, SEMANTIC, NONE
        self.similarity_score = similarity_score


class QuestionDeduplicator:
    """Detects duplicates and merges metadata into canonical questions."""

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def _tokenize(text: str) -> set:
        """Tokenize text into lowercase alphanumeric words."""
        words = re.findall(r"\b[a-z0-9_]{2,}\b", text.lower())
        return set(words)

    @staticmethod
    def _shingle_ngrams(text: str, n: int = 3) -> set:
        """Create character n-grams for typo-resistant similarity."""
        clean = re.sub(r"\s+", " ", text.lower().strip())
        if len(clean) < n:
            return {clean}
        return {clean[i:i+n] for i in range(len(clean) - n + 1)}

    def calculate_similarity(self, text_a: str, text_b: str) -> float:
        """
        Combines word token Dice similarity, token overlap, and character 3-gram similarity.
        Yields robust semantic similarity score in [0.0, 1.0].
        """
        norm_a = QuestionNormalizer.normalize_text(text_a)
        norm_b = QuestionNormalizer.normalize_text(text_b)

        if norm_a == norm_b:
            return 1.0

        tokens_a = self._tokenize(norm_a)
        tokens_b = self._tokenize(norm_b)

        if not tokens_a or not tokens_b:
            return 0.0

        # Word Token Dice similarity: 2 * |A ∩ B| / (|A| + |B|)
        intersection_len = len(tokens_a.intersection(tokens_b))
        token_dice = (2.0 * intersection_len) / (len(tokens_a) + len(tokens_b))

        # Word Token Overlap (containment): |A ∩ B| / min(|A|, |B|)
        token_overlap = intersection_len / min(len(tokens_a), len(tokens_b))

        # Shingle n-gram Jaccard for character-level structure
        shingles_a = self._shingle_ngrams(norm_a, n=3)
        shingles_b = self._shingle_ngrams(norm_b, n=3)
        ngram_intersection = len(shingles_a.intersection(shingles_b))
        ngram_union = len(shingles_a.union(shingles_b))
        ngram_jaccard = ngram_intersection / ngram_union if ngram_union > 0 else 0.0

        # Weighted combination: 50% Dice, 30% Overlap, 20% n-gram
        return 0.50 * token_dice + 0.30 * token_overlap + 0.20 * ngram_jaccard

    def check_duplicate(self, candidate_question: Question, existing_questions: List[Question]) -> DeduplicationResult:
        """
        Compares candidate question against an existing list of questions.
        Tier 1: Check identical content_hash (Exact match).
        Tier 2: Check semantic similarity across existing questions in same category (Semantic match).
        """
        # Tier 1: Exact Hash Check
        for existing in existing_questions:
            if existing.content_hash == candidate_question.content_hash:
                return DeduplicationResult(
                    is_duplicate=True,
                    canonical_question=existing,
                    match_type="EXACT",
                    similarity_score=1.0,
                )

        # Tier 2: Semantic check within same high-level category
        best_match = None
        best_score = 0.0

        for existing in existing_questions:
            # We constrain semantic matching to same category to prevent false positives
            if existing.category == candidate_question.category:
                sim = self.calculate_similarity(
                    candidate_question.problem_statement,
                    existing.problem_statement
                )
                if sim > best_score:
                    best_score = sim
                    best_match = existing

        if best_match and best_score >= self.similarity_threshold:
            return DeduplicationResult(
                is_duplicate=True,
                canonical_question=best_match,
                match_type="SEMANTIC",
                similarity_score=best_score,
            )

        return DeduplicationResult(is_duplicate=False, similarity_score=best_score)

    @staticmethod
    def merge_into_canonical(canonical: Question, duplicate: Question) -> Question:
        """
        Merges duplicate question metadata into canonical question:
        - Increments observed_frequency
        - Appends new unique sources
        - Updates source_count
        - Merges companies and roles
        - Updates first_seen and last_seen timestamps
        - Merges skills
        """
        # Update frequencies
        canonical.observed_frequency += duplicate.observed_frequency

        # Merge companies (case-insensitive deduplication)
        comp_set = {c.strip() for c in canonical.companies if c.strip()}
        for c in duplicate.companies:
            if c.strip() and c.strip().lower() not in {x.lower() for x in comp_set}:
                comp_set.add(c.strip())
        canonical.companies = sorted(list(comp_set))

        # Merge roles
        role_set = {r.strip() for r in canonical.roles if r.strip()}
        for r in duplicate.roles:
            if r.strip() and r.strip().lower() not in {x.lower() for x in role_set}:
                role_set.add(r.strip())
        canonical.roles = sorted(list(role_set))

        # Merge skills
        skill_set = set(canonical.skills)
        for s in duplicate.skills:
            if s.strip():
                skill_set.add(s.strip())
        canonical.skills = sorted(list(skill_set))

        # Merge sources and preserve attribution
        existing_source_keys = {
            f"{s.source_name}_{s.source_item_id or ''}" for s in canonical.sources
        }
        for s in duplicate.sources:
            k = f"{s.source_name}_{s.source_item_id or ''}"
            if k not in existing_source_keys:
                canonical.sources.append(s)
                existing_source_keys.add(k)

        # Source count is count of distinct source providers
        distinct_source_names = {s.source_name for s in canonical.sources}
        canonical.source_count = max(len(distinct_source_names), canonical.source_count + 1)

        # Update timestamps
        # first_seen is min
        if duplicate.first_seen < canonical.first_seen:
            canonical.first_seen = duplicate.first_seen
        # last_seen is max
        if duplicate.last_seen > canonical.last_seen:
            canonical.last_seen = duplicate.last_seen
        else:
            canonical.last_seen = datetime.now(timezone.utc).isoformat()

        canonical.updated_at = datetime.now(timezone.utc).isoformat()
        return canonical
