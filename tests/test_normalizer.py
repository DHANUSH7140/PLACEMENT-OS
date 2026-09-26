"""
Unit Tests for Question Normalizer.
"""

from data_pipeline.intelligence.normalizer import QuestionNormalizer


def test_text_normalization():
    raw = "   Problem Statement:  Given a ‘singly linked list’, reverse it…   "
    normalized = QuestionNormalizer.normalize_text(raw)
    assert "Problem Statement:" not in normalized
    assert "‘" not in normalized
    assert "'" in normalized
    assert "..." in normalized
    assert normalized == "Given a 'singly linked list', reverse it..."


def test_content_hash_determinism():
    text1 = "Given weights and values of N items, put these items in a knapsack of capacity W."
    text2 = "Problem Statement: Given weights and values of N items, put these items in a knapsack of capacity W."
    hash1 = QuestionNormalizer.generate_content_hash(text1)
    hash2 = QuestionNormalizer.generate_content_hash(text2)
    assert hash1 == hash2


def test_clean_title():
    t1 = "1. Two Sum Problem"
    t2 = "Problem 42 - Longest Common Subsequence"
    assert QuestionNormalizer.clean_title(t1) == "Two Sum Problem"
    assert QuestionNormalizer.clean_title(t2) == "Longest Common Subsequence"
