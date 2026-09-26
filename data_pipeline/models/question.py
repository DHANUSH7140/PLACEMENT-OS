"""
Question Data Model & Schemas for Firestore.
Complies with the Placement OS Canonical Question Schema and Firestore constraints.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    __test__ = False  # Prevents pytest from attempting to collect this data model as a test suite
    input: str
    expected_output: str
    is_hidden: bool = False
    explanation: Optional[str] = None


class QuestionSource(BaseModel):
    source_name: str
    source_url: Optional[str] = None
    source_item_id: Optional[str] = None
    discovered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    attribution: Optional[str] = None


class Question(BaseModel):
    # Required core schema fields as specified
    id: str = Field(..., description="Unique question identifier: q_hash or q_uuid")
    category: str = Field(..., description="High level taxonomy category, e.g. DSA, SQL, OS, etc.")
    subcategory: str = Field(..., description="Specific subcategory, e.g. Dynamic Programming")
    topic: str = Field(..., description="Specific topic, e.g. Knapsack")
    skills: List[str] = Field(default_factory=list, description="Skills tested by this question")
    question_type: str = Field(default="Coding", description="Coding, MCQ, Subjective, SystemDesign, Behavioral")
    difficulty: str = Field(default="Medium", description="Easy, Medium, or Hard")
    companies: List[str] = Field(default_factory=list, description="Companies observing or asking this question")
    roles: List[str] = Field(default_factory=list, description="Roles targeted, e.g. SDE-1, Data Analyst")
    observed_frequency: int = Field(default=1, description="Observed occurrence count across monitored sources")
    source_count: int = Field(default=1, description="Number of distinct sources mentioning this question")
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    student_relevance: float = Field(default=0.0, description="Dynamically computed relevance score (0.0 - 1.0)")

    # Full Question Content & Student Experience
    title: str = Field(..., description="Concise question title")
    problem_statement: str = Field(..., description="Clear, normalized problem description")
    explanation: Optional[str] = Field(default=None, description="Core concept explanation")
    options: Optional[List[str]] = Field(default=None, description="Multiple choice options if MCQ")
    correct_answer: Optional[str] = Field(default=None, description="Correct option index or short answer")
    solution_approach: Optional[str] = Field(default=None, description="Step-by-step logic and time/space complexity")
    code_snippets: Dict[str, str] = Field(default_factory=dict, description="Boilerplate code per language: python, java, cpp")
    test_cases: List[TestCase] = Field(default_factory=list, description="Sample and validation test cases")
    learning_hints: List[str] = Field(default_factory=list, description="Progressive hints generated to avoid direct spoilers")

    # Ingestion & Integrity Metadata
    content_hash: str = Field(..., description="SHA-256 hash of normalized text for exact deduplication")
    sources: List[QuestionSource] = Field(default_factory=list, description="Attributed sources")
    is_active: bool = Field(default=True, description="Soft-delete or visibility toggle")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        """Convert to clean dictionary ready for Firestore document write."""
        return self.model_dump()


class QuestionAttempt(BaseModel):
    id: str = Field(..., description="qa_...")
    student_id: str = Field(..., description="User UID from student_profiles")
    question_id: str = Field(..., description="Reference to questions/{question_id}")
    assessment_id: Optional[str] = Field(default=None, description="Reference if attempted within an assessment")
    status: str = Field(..., description="PASSED, FAILED, PARTIAL, SKIPPED")
    submitted_code_or_answer: str = Field(...)
    language: Optional[str] = Field(default="python")
    execution_time_ms: Optional[float] = Field(default=None)
    memory_used_kb: Optional[float] = Field(default=None)
    score: float = Field(default=0.0, description="Normalized score 0.0 - 100.0")
    feedback: Optional[str] = Field(default=None)
    time_taken_seconds: int = Field(default=0)
    attempted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class Mistake(BaseModel):
    id: str = Field(..., description="m_...")
    student_id: str = Field(..., description="User UID")
    question_id: str = Field(..., description="Reference to questions/{question_id}")
    attempt_id: str = Field(..., description="Reference to question_attempts/{attempt_id}")
    category: str = Field(..., description="DSA, SQL, OS, etc.")
    subcategory: str = Field(...)
    mistake_type: str = Field(..., description="Syntax, Logic, EdgeCase, TimeLimitExceeded, Conceptual")
    student_notes: Optional[str] = Field(default="")
    ai_diagnosis: Optional[str] = Field(default=None)
    recommended_revision_date: Optional[str] = Field(default=None)
    is_resolved: bool = Field(default=False)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()
