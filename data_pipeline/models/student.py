"""
User, Student Profile, Learning Plan, and Event Data Models for Firestore.
Provides contract consistency across Member 1 (Frontend) and Member 2 (FastAPI).
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class User(BaseModel):
    uid: str = Field(..., description="Firebase Authentication UID")
    email: str = Field(...)
    display_name: Optional[str] = Field(default="")
    photo_url: Optional[str] = Field(default=None)
    role: str = Field(default="student", description="student, mentor, admin")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_login: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_active: bool = Field(default=True)

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class StudentProfile(BaseModel):
    student_id: str = Field(..., description="Matches User UID")
    full_name: str = Field(...)
    college_name: Optional[str] = Field(default="University Institute of Technology")
    branch: Optional[str] = Field(default="Computer Science and Engineering")
    graduation_year: int = Field(default=2026)
    cgpa: float = Field(default=8.5)
    
    # Career Targets
    target_companies: List[str] = Field(default_factory=lambda: ["Google", "Amazon", "Microsoft"])
    target_roles: List[str] = Field(default_factory=lambda: ["Software Engineer", "SDE-1"])
    preferred_languages: List[str] = Field(default_factory=lambda: ["Python", "Java", "C++"])

    # Computed Readiness & Analytics
    readiness_score: float = Field(default=68.5, description="Aggregate placement readiness score 0.0 - 100.0")
    total_questions_solved: int = Field(default=0)
    category_progress: Dict[str, float] = Field(default_factory=dict, description="e.g. {'DSA': 72.0, 'SQL': 80.0}")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)

    # Document references
    resume_document_id: Optional[str] = Field(default=None, description="Reference to documents/{doc_id}")
    active_learning_plan_id: Optional[str] = Field(default=None)

    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class LearningTask(BaseModel):
    task_id: str
    title: str
    category: str
    target_type: str = "question"  # question, reading, mock_interview
    target_id: Optional[str] = None
    is_completed: bool = False
    completed_at: Optional[str] = None


class Milestone(BaseModel):
    milestone_id: str
    title: str
    description: str
    due_date: str
    is_completed: bool = False
    tasks: List[LearningTask] = Field(default_factory=list)


class LearningPlan(BaseModel):
    id: str = Field(..., description="lp_...")
    student_id: str = Field(..., description="User UID")
    title: str = Field(default="Placement Readiness 60-Day Sprint")
    target_company: Optional[str] = Field(default=None)
    target_role: Optional[str] = Field(default="Software Development Engineer")
    start_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_completion_date: str = Field(...)
    completion_percentage: float = Field(default=0.0)
    status: str = Field(default="ACTIVE", description="ACTIVE, PAUSED, COMPLETED")
    milestones: List[Milestone] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class Event(BaseModel):
    id: str = Field(..., description="evt_...")
    student_id: str = Field(...)
    event_type: str = Field(..., description="QUESTION_VIEW, ATTEMPT_SUBMIT, HINT_CLICK, INTERVIEW_START, etc.")
    session_id: Optional[str] = Field(default=None)
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()
