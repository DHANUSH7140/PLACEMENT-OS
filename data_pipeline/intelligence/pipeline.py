"""
Question Intelligence Pipeline Orchestrator.
Executes the full pipeline stages:
Discovery -> Extraction -> Normalization -> Exact Deduplication -> Semantic Deduplication
-> Classification -> Company Tagging -> Role Tagging -> Difficulty -> Observed Frequency
-> Gemini Enrichment -> Firestore -> Available to Student
"""

import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from ..models.question import Question, QuestionSource
from .normalizer import QuestionNormalizer
from .deduplicator import QuestionDeduplicator
from .classifier import TaxonomyClassifier
from .tagger import EntityTagger
from .difficulty import DifficultyEstimator
from .gemini_enricher import GeminiEnricher

logger = logging.getLogger(__name__)


class IngestionItem:
    """Raw question payload extracted from a source before pipeline processing."""
    def __init__(
        self,
        raw_text: str,
        title: str = "",
        source_name: str = "curated_feed",
        source_url: Optional[str] = None,
        source_item_id: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        companies: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        question_type: str = "Coding",
        options: Optional[List[str]] = None,
        correct_answer: Optional[str] = None,
        observed_frequency: int = 1,
    ):
        self.raw_text = raw_text
        self.title = title
        self.source_name = source_name
        self.source_url = source_url
        self.source_item_id = source_item_id
        self.category = category
        self.subcategory = subcategory
        self.topic = topic
        self.difficulty = difficulty
        self.companies = companies or []
        self.roles = roles or []
        self.question_type = question_type
        self.options = options
        self.correct_answer = correct_answer
        self.observed_frequency = observed_frequency


class QuestionIntelligencePipeline:
    """End-to-end question processing, normalization, deduplication, and enrichment."""

    def __init__(self, similarity_threshold: float = 0.85):
        self.normalizer = QuestionNormalizer()
        self.deduplicator = QuestionDeduplicator(similarity_threshold=similarity_threshold)
        self.enricher = GeminiEnricher()

    def process_item(self, item: IngestionItem, existing_questions: List[Question]) -> Dict[str, Any]:
        """
        Processes a single IngestionItem through all stages of the pipeline.
        Returns a dictionary with status and the canonical/new Question.
        """
        # Step 1: Normalization
        norm_text = self.normalizer.normalize_text(item.raw_text)
        content_hash = self.normalizer.generate_content_hash(norm_text)
        clean_title = self.normalizer.clean_title(item.title or norm_text[:60])

        # Step 2: Classification (if not pre-specified)
        if not item.category or item.category not in TaxonomyClassifier.TAXONOMY_KEYWORDS:
            cat, subcat, topic, detected_skills = TaxonomyClassifier.classify(norm_text, clean_title)
        else:
            cat = item.category
            subcat = item.subcategory or "General"
            topic = item.topic or subcat
            _, _, _, detected_skills = TaxonomyClassifier.classify(norm_text, clean_title)

        # Step 3: Company & Role Tagging
        companies, roles = EntityTagger.tag_companies_and_roles(
            norm_text,
            category=cat,
            existing_companies=item.companies,
            existing_roles=item.roles
        )

        # Step 4: Difficulty Estimation
        difficulty = DifficultyEstimator.estimate_difficulty(
            norm_text,
            category=cat,
            subcategory=subcat,
            explicit_difficulty=item.difficulty
        )

        # Step 5: Source Tracking & Attribution
        now_iso = datetime.now(timezone.utc).isoformat()
        source_obj = QuestionSource(
            source_name=item.source_name,
            source_url=item.source_url,
            source_item_id=item.source_item_id,
            discovered_at=now_iso,
            attribution=f"Discovered via {item.source_name}"
        )

        # Step 6: Create Candidate Question Model
        # Note: id format is q_{first 16 chars of hash}
        q_id = f"q_{content_hash[:16]}"
        candidate = Question(
            id=q_id,
            category=cat,
            subcategory=subcat,
            topic=topic,
            skills=detected_skills,
            question_type=item.question_type,
            difficulty=difficulty,
            companies=companies,
            roles=roles,
            observed_frequency=item.observed_frequency,
            source_count=1,
            first_seen=now_iso,
            last_seen=now_iso,
            student_relevance=0.0,
            title=clean_title,
            problem_statement=norm_text,
            options=item.options,
            correct_answer=item.correct_answer,
            content_hash=content_hash,
            sources=[source_obj],
            created_at=now_iso,
            updated_at=now_iso,
        )

        # Step 7: Deduplication (Exact & Semantic)
        dedup_result = self.deduplicator.check_duplicate(candidate, existing_questions)

        if dedup_result.is_duplicate and dedup_result.canonical_question:
            # Merge into canonical
            merged = self.deduplicator.merge_into_canonical(dedup_result.canonical_question, candidate)
            # Recompute student relevance
            merged.student_relevance = DifficultyEstimator.calculate_student_relevance(
                merged.observed_frequency,
                merged.source_count,
                merged.difficulty,
                len(merged.companies)
            )
            return {
                "action": "MERGED",
                "match_type": dedup_result.match_type,
                "similarity_score": dedup_result.similarity_score,
                "question": merged
            }

        # Step 8: Gemini Enrichment for new question
        candidate.student_relevance = DifficultyEstimator.calculate_student_relevance(
            candidate.observed_frequency,
            candidate.source_count,
            candidate.difficulty,
            len(candidate.companies)
        )
        enrichment = self.enricher.enrich(
            candidate.title,
            candidate.problem_statement,
            candidate.category,
            candidate.subcategory,
            candidate.difficulty
        )
        candidate.explanation = enrichment.get("explanation")
        candidate.solution_approach = enrichment.get("solution_approach")
        candidate.learning_hints = enrichment.get("learning_hints", [])
        candidate.test_cases = enrichment.get("test_cases", [])

        # Add to existing questions in memory
        existing_questions.append(candidate)

        return {
            "action": "INSERTED",
            "match_type": "NEW",
            "similarity_score": 0.0,
            "question": candidate
        }

    def process_batch(self, items: List[IngestionItem], existing_questions: List[Question]) -> Dict[str, Any]:
        """Processes a batch of IngestionItems."""
        inserted = 0
        merged = 0
        exact_dupes = 0
        semantic_dupes = 0

        for item in items:
            res = self.process_item(item, existing_questions)
            if res["action"] == "INSERTED":
                inserted += 1
            elif res["action"] == "MERGED":
                merged += 1
                if res["match_type"] == "EXACT":
                    exact_dupes += 1
                elif res["match_type"] == "SEMANTIC":
                    semantic_dupes += 1

        return {
            "total_processed": len(items),
            "inserted": inserted,
            "merged": merged,
            "exact_duplicates": exact_dupes,
            "semantic_duplicates": semantic_dupes,
            "final_question_count": len(existing_questions)
        }
