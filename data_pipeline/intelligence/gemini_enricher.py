"""
Gemini Question Enrichment Service.
Uses Gemini AI to generate original explanations, structured solution approaches,
clean test cases, and progressive learning hints without reproducing copyrighted text.
Includes deterministic offline fallbacks so the pipeline functions even when an API key is omitted.
"""

import json
import logging
from typing import List, Optional, Dict, Any
from ..config import GEMINI_API_KEY, GEMINI_MODEL, ENABLE_GEMINI_ENRICHMENT
from ..models.question import TestCase

logger = logging.getLogger(__name__)


class GeminiEnricher:
    """Enriches questions with original educational hints, solution outlines, and test cases."""

    def __init__(self, api_key: str = GEMINI_API_KEY, model_name: str = GEMINI_MODEL):
        self.api_key = api_key
        self.model_name = model_name
        self.enabled = ENABLE_GEMINI_ENRICHMENT and bool(self.api_key)

    def enrich(self, title: str, problem_statement: str, category: str, subcategory: str, difficulty: str) -> Dict[str, Any]:
        """
        Enriches a question.
        Returns:
            {
                "explanation": str,
                "solution_approach": str,
                "learning_hints": List[str],
                "test_cases": List[TestCase]
            }
        """
        if self.enabled:
            try:
                return self._enrich_via_gemini_api(title, problem_statement, category, subcategory, difficulty)
            except Exception as e:
                logger.warning(f"Gemini enrichment API call failed: {e}. Falling back to deterministic enrichment.")

        return self._generate_fallback_enrichment(title, problem_statement, category, subcategory, difficulty)

    def _enrich_via_gemini_api(self, title: str, problem: str, category: str, subcategory: str, difficulty: str) -> Dict[str, Any]:
        """Calls Gemini API to generate structured educational aids."""
        import urllib.request

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        prompt = f"""
You are an expert technical interviewer and educator for college placement preparation.
Given the following interview question, generate original educational aids in valid JSON format:

Title: {title}
Category: {category} ({subcategory})
Difficulty: {difficulty}
Problem: {problem}

Return ONLY valid JSON matching this schema:
{{
  "explanation": "Clear explanation of the core concept and what interviewers test here",
  "solution_approach": "Step-by-step optimal strategy with Time and Space complexity analysis",
  "learning_hints": [
    "Hint 1 (Conceptual nudge without giving answer)",
    "Hint 2 (Data structure or algorithmic hint)",
    "Hint 3 (Edge case or optimal transition hint)"
  ],
  "test_cases": [
    {{"input": "sample input 1", "expected_output": "sample output 1", "is_hidden": false, "explanation": "base case"}},
    {{"input": "sample input 2", "expected_output": "sample output 2", "is_hidden": true, "explanation": "edge case"}}
  ]
}}
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "responseMimeType": "application/json"}
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(content)

            test_cases = [
                TestCase(
                    input=tc.get("input", ""),
                    expected_output=tc.get("expected_output", ""),
                    is_hidden=tc.get("is_hidden", False),
                    explanation=tc.get("explanation")
                )
                for tc in parsed.get("test_cases", [])
            ]

            return {
                "explanation": parsed.get("explanation", ""),
                "solution_approach": parsed.get("solution_approach", ""),
                "learning_hints": parsed.get("learning_hints", []),
                "test_cases": test_cases
            }

    def _generate_fallback_enrichment(self, title: str, problem: str, category: str, subcategory: str, difficulty: str) -> Dict[str, Any]:
        """Provides high-quality, pedagogically structured enrichment offline."""
        explanation = f"Evaluates core proficiency in {category} with an emphasis on {subcategory}. Interviewers seek clean problem breakdown, optimal algorithmic complexity, and edge-case handling."
        solution = f"1. Analyze problem constraints and identify invariant properties.\n2. Consider brute-force approach then optimize using {subcategory} concepts.\n3. Validate edge cases (e.g. empty bounds, single element, negative values).\n4. Aim for optimal Time and Space complexity."
        
        hints = [
            f"Think about how {subcategory} techniques can eliminate redundant computations.",
            "Can you write down the state representation or relation for smaller inputs?",
            "Ensure you account for empty inputs and boundary constraints."
        ]

        sample_cases = [
            TestCase(input="Sample input representative of standard case", expected_output="Expected canonical output", is_hidden=False, explanation="Standard test condition"),
            TestCase(input="Boundary case (e.g. 0 or empty)", expected_output="Expected base output", is_hidden=True, explanation="Edge case verification")
        ]

        return {
            "explanation": explanation,
            "solution_approach": solution,
            "learning_hints": hints,
            "test_cases": sample_cases
        }
