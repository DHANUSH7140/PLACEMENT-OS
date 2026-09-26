"""
Assessment and Interview Data Models for Firestore.
Provides consistency for Member 1 (Frontend UI) and Member 2 (FastAPI Evaluation Engine).
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Assessment(BaseModel):
    id: str = Field(..., description="asm_...")
    student_id: str = Field(..., description="Target student UID")
    title: str = Field(...)
    assessment_type: str = Field(default="TOPIC_TEST", description="DIAGNOSTIC, COMPANY_MOCK, TOPIC_TEST, COMPREHENSIVE")
    company: Optional[str] = Field(default=None)
    role: Optional[str] = Field(default=None)
    question_ids: List[str] = Field(default_factory=list)
    time_limit_minutes: int = Field(default=60)
    status: str = Field(default="PENDING", description="PENDING, IN_PROGRESS, COMPLETED, EXPIRED")
    score: Optional[float] = Field(default=None, description="Score 0 - 100")
    total_questions: int = Field(default=0)
    passed_questions: int = Field(default=0)
    category_scores: Dict[str, float] = Field(default_factory=dict)
    feedback: Optional[str] = Field(default=None)
    started_at: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class InterviewTurn(BaseModel):
    speaker: str = Field(..., description="ai_interviewer or student")
    message: str = Field(...)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evaluation_notes: Optional[str] = None


class RubricScores(BaseModel):
    problem_solving: float = Field(default=0.0)
    technical_depth: float = Field(default=0.0)
    communication: float = Field(default=0.0)
    system_architecture: Optional[float] = None
    culture_fit: Optional[float] = None


class Interview(BaseModel):
    id: str = Field(..., description="intv_...")
    student_id: str = Field(..., description="Student UID")
    interview_type: str = Field(default="TECHNICAL", description="TECHNICAL, HR_BEHAVIORAL, SYSTEM_DESIGN, RESUME_DEEP_DIVE")
    target_company: Optional[str] = Field(default=None)
    target_role: Optional[str] = Field(default="SDE-1")
    status: str = Field(default="SCHEDULED", description="SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED")
    duration_minutes: int = Field(default=45)
    turns: List[InterviewTurn] = Field(default_factory=list)
    rubric_scores: RubricScores = Field(default_factory=RubricScores)
    overall_score: Optional[float] = Field(default=None)
    strengths_identified: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    detailed_feedback: Optional[str] = Field(default=None)
    started_at: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()
