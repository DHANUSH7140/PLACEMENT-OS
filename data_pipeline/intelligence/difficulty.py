"""
Difficulty and Complexity Estimator.
Classifies questions into 'Easy', 'Medium', or 'Hard' based on algorithmic constraints,
cognitive load, concept prerequisites, and statement length.
Also computes baseline student relevance score.
"""

import re
from typing import Tuple


class DifficultyEstimator:
    """Estimates difficulty and student placement relevance."""

    HARD_INDICATORS = [
        "hard", "advanced", "dynamic programming", "segment tree", "trie",
        "fenwick tree", "graph coloring", "strongly connected", "np-hard",
        "o(n log n)", "cap theorem", "byzantine", "concurrency control",
        "distributed transaction", "transformer architecture", "attention head",
        "two phase commit", "red-black tree", "disjoint set union"
    ]

    MEDIUM_INDICATORS = [
        "medium", "intermediate", "binary search", "bfs", "dfs", "recursion",
        "memoization", "stack", "queue", "hashmap", "sliding window",
        "two pointer", "linked list cycle", "join", "window function",
        "normalization", "deadlock", "paging", "tcp handshake", "polymorphism",
        "logistic regression", "random forest", "pca", "dockerfile", "indexing"
    ]

    EASY_INDICATORS = [
        "easy", "beginner", "basic", "loop", "array", "string reversal",
        "linear search", "bubble sort", "even odd", "prime number", "palindrome",
        "select query", "where clause", "primary key", "what is", "define",
        "explain the difference", "acid properties", "osi layers"
    ]

    @classmethod
    def estimate_difficulty(cls, text: str, category: str, subcategory: str, explicit_difficulty: str = None) -> str:
        """Determines Easy, Medium, or Hard difficulty."""
        if explicit_difficulty and explicit_difficulty.strip().title() in ["Easy", "Medium", "Hard"]:
            return explicit_difficulty.strip().title()

        content = f"{text} {category} {subcategory}".lower()

        hard_score = sum(1 for term in cls.HARD_INDICATORS if term in content)
        medium_score = sum(1 for term in cls.MEDIUM_INDICATORS if term in content)
        easy_score = sum(1 for term in cls.EASY_INDICATORS if term in content)

        # Behavioral and HR questions are predominantly Medium in placement interviews
        if category in ["HR", "Behavioral", "Communication", "Resume"]:
            return "Medium"

        if hard_score >= 2 or (hard_score > medium_score and hard_score > easy_score):
            return "Hard"
        elif medium_score >= 1 or len(text) > 400:
            return "Medium"
        else:
            return "Easy"

    @classmethod
    def calculate_student_relevance(cls, observed_frequency: int, source_count: int, difficulty: str, company_count: int) -> float:
        """
        Computes student_relevance in [0.0, 1.0].
        Favors questions with multi-source recurrence, top company appearance,
        and interview suitability.
        """
        freq_factor = min(observed_frequency / 10.0, 1.0) * 0.40
        source_factor = min(source_count / 5.0, 1.0) * 0.30
        company_factor = min(company_count / 4.0, 1.0) * 0.20
        diff_weight = {"Easy": 0.07, "Medium": 0.10, "Hard": 0.08}.get(difficulty, 0.08)

        relevance = freq_factor + source_factor + company_factor + diff_weight
        return round(min(max(relevance, 0.1), 1.0), 3)
