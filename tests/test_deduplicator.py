"""
Unit Tests for Deduplication Engine.
"""

from data_pipeline.models.question import Question, QuestionSource
from data_pipeline.intelligence.deduplicator import QuestionDeduplicator
from data_pipeline.intelligence.normalizer import QuestionNormalizer


def test_exact_hash_deduplication():
    dedup = QuestionDeduplicator(similarity_threshold=0.85)
    text = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
    h = QuestionNormalizer.generate_content_hash(text)

    q1 = Question(
        id="q_1",
        category="DSA",
        subcategory="Arrays",
        topic="Two Sum",
        title="Two Sum",
        problem_statement=text,
        content_hash=h,
        companies=["Amazon"],
        roles=["SDE-1"],
        observed_frequency=1,
        source_count=1,
    )

    q2 = Question(
        id="q_2",
        category="DSA",
        subcategory="Arrays",
        topic="Two Sum",
        title="Two Sum Problem",
        problem_statement=text,
        content_hash=h,
        companies=["Google"],
        roles=["Software Engineer"],
        observed_frequency=1,
        source_count=1,
    )

    result = dedup.check_duplicate(q2, [q1])
    assert result.is_duplicate is True
    assert result.match_type == "EXACT"

    # Test merge
    merged = dedup.merge_into_canonical(q1, q2)
    assert merged.observed_frequency == 2
    assert "Amazon" in merged.companies
    assert "Google" in merged.companies
    assert "SDE-1" in merged.roles
    assert "Software Engineer" in merged.roles


def test_semantic_deduplication():
    dedup = QuestionDeduplicator(similarity_threshold=0.75)
    text_a = "Given weights and values of N items, put these items in a knapsack of capacity W to get maximum total value in knapsack."
    text_b = "Given values and weights of N items, place these items into a knapsack of capacity W to achieve the maximum total value."

    h_a = QuestionNormalizer.generate_content_hash(text_a)
    h_b = QuestionNormalizer.generate_content_hash(text_b)

    assert h_a != h_b  # Hashes differ due to slight wording change

    q1 = Question(
        id="q_1",
        category="DSA",
        subcategory="Dynamic Programming",
        topic="Knapsack",
        title="0/1 Knapsack",
        problem_statement=text_a,
        content_hash=h_a,
        companies=["Amazon"],
    )

    q2 = Question(
        id="q_2",
        category="DSA",
        subcategory="Dynamic Programming",
        topic="Knapsack",
        title="Knapsack Problem",
        problem_statement=text_b,
        content_hash=h_b,
        companies=["Microsoft"],
    )

    result = dedup.check_duplicate(q2, [q1])
    assert result.is_duplicate is True
    assert result.match_type == "SEMANTIC"
    assert result.similarity_score >= 0.75
