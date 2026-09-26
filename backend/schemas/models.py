from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Health
class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    services: Dict[str, str] = Field(default_factory=dict)

# Readiness Dimensions
class ReadinessDimensions(BaseModel):
    aptitude: float = 50.0
    dsa: float = 50.0
    cs_fundamentals: float = 50.0
    sql: float = 50.0
    communication: float = 50.0
    resume: float = 50.0
    projects: float = 50.0
    interview: float = 50.0

class NextBestAction(BaseModel):
    action_id: str
    title: str
    type: str  # e.g., "practice_topic", "take_assessment", "mock_interview", "resume_fix"
    description: str
    target_dimension: str
    estimated_minutes: int
    priority: str  # "high", "medium", "low"

class ReadinessResult(BaseModel):
    overall_score: float
    dimensions: ReadinessDimensions
    strengths: List[str] = Field(default_factory=list)
    critical_gaps: List[str] = Field(default_factory=list)
    risk_areas: List[str] = Field(default_factory=list)
    next_best_action: Optional[NextBestAction] = None

# Student Profile & Onboarding
class StudentProfileOnboard(BaseModel):
    user_id: str
    name: str
    email: str
    target_role: str  # e.g., "Backend Engineer", "Full Stack Developer", "Data Engineer"
    target_company: Optional[str] = "Tier 1 Product Company"
    preparation_weeks: int = 12
    current_year_or_exp: Optional[str] = "Final Year CS"
    known_skills: List[str] = Field(default_factory=list)

class StudentProfileResponse(BaseModel):
    user_id: str
    name: str
    email: str
    target_role: str
    target_company: str
    readiness: ReadinessResult
    created_at: str
    updated_at: str

# Placement Route / GPS
class RouteNode(BaseModel):
    step_id: str
    title: str
    category: str  # "Aptitude", "DSA", "SQL", "Interview", "Project", "Resume"
    topics: List[str]
    status: str  # "completed", "in_progress", "pending", "locked"
    estimated_hours: int

class PlacementGPSRoute(BaseModel):
    user_id: str
    current_state: str
    destination: str
    route: List[RouteNode]
    blocked_by: List[str] = Field(default_factory=list)
    next_action: Optional[NextBestAction] = None
    route_status: str = "on_track"  # "on_track", "needs_recalculation", "behind"
    last_recalculated_at: str

# Dashboard
class DashboardResponse(BaseModel):
    user_id: str
    student_name: str
    target_role: str
    target_company: str
    readiness: ReadinessResult
    placement_route: PlacementGPSRoute
    active_missions: List[Dict[str, Any]] = Field(default_factory=list)
    recent_mistakes_count: int = 0

# Questions & Attempts
class QuestionItem(BaseModel):
    question_id: str
    title: str
    topic: str
    category: str
    difficulty: str  # "Easy", "Medium", "Hard"
    content: str
    options: Optional[List[str]] = None
    correct_option_index: Optional[int] = None
    explanation: Optional[str] = None

class QuestionAttemptRequest(BaseModel):
    user_id: str
    question_id: str
    submitted_answer: str
    time_taken_seconds: int

class QuestionAttemptResponse(BaseModel):
    attempt_id: str
    user_id: str
    question_id: str
    is_correct: bool
    score: float
    feedback: str
    correct_answer: str
    explanation: str
    mistake_logged: bool = False

# Assessment
class AssessmentStartRequest(BaseModel):
    user_id: str
    category: str  # e.g., "DSA", "Aptitude", "SQL", "CS Fundamentals", "Full Mock"
    question_count: int = 5

class AssessmentStartResponse(BaseModel):
    assessment_id: str
    user_id: str
    category: str
    questions: List[QuestionItem]
    created_at: str

class AssessmentAnswerSubmission(BaseModel):
    question_id: str
    submitted_answer: str
    time_taken_seconds: int

class AssessmentSubmitRequest(BaseModel):
    user_id: str
    answers: List[AssessmentAnswerSubmission]

class AssessmentSubmitResponse(BaseModel):
    assessment_id: str
    overall_score: float
    total_questions: int
    correct_count: int
    dimension_impacts: Dict[str, float]
    feedback_summary: str
    new_skill_gaps: List[str]
    route_recalculated: bool = False

# AI Interview
class InterviewStartRequest(BaseModel):
    user_id: str
    interview_type: str  # "technical", "HR", "behavioral", "project", "resume", "role_specific"
    target_role: Optional[str] = None
    target_company: Optional[str] = None

class InterviewStartResponse(BaseModel):
    interview_id: str
    user_id: str
    interview_type: str
    current_question_number: int
    question: str
    context_notes: str

class InterviewAnswerRequest(BaseModel):
    user_id: str
    candidate_answer: str

class InterviewEvaluation(BaseModel):
    correctness: float
    technical_depth: float
    clarity: float
    relevance: float
    structure: float
    conciseness: float
    overall_answer_score: float
    feedback: str
    key_strengths: List[str]
    improvement_areas: List[str]

class InterviewAnswerResponse(BaseModel):
    interview_id: str
    evaluation: InterviewEvaluation
    is_completed: bool
    next_question: Optional[str] = None
    interview_summary: Optional[Dict[str, Any]] = None

# Resume Intelligence
class ResumeAnalyzeRequest(BaseModel):
    user_id: str
    resume_text: str

class ResumeAnalyzeResponse(BaseModel):
    user_id: str
    extracted_skills: List[str]
    projects: List[Dict[str, Any]]
    technologies: List[str]
    experience: List[Dict[str, Any]]
    achievements: List[str]
    resume_score: float
    improvement_suggestions: List[str]
    resume_grounded_questions: List[str]

# Project Intelligence
class ProjectAnalyzeRequest(BaseModel):
    user_id: str
    project_title: str
    project_description: str
    tech_stack: List[str]
    architecture_overview: Optional[str] = None

class ProjectAnalyzeResponse(BaseModel):
    user_id: str
    project_title: str
    complexity_score: float
    strengths: List[str]
    weaknesses: List[str]
    architectural_feedback: str
    suggested_enhancements: List[str]
    potential_interview_questions: List[str]

# Job Match
class JobMatchRequest(BaseModel):
    user_id: str
    resume_text: str
    job_description: str

class JobMatchResponse(BaseModel):
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    evidence: List[str]
    recommendations: List[str]

# Mistakes
class MistakeRecord(BaseModel):
    mistake_id: str
    user_id: str
    topic: str
    question_id: Optional[str] = None
    question_text: str
    mistake_type: str  # "conceptual", "syntax", "edge_case", "time_limit", "misinterpretation"
    likely_cause: str
    correction: str
    remediation: str
    recurrence_count: int = 1
    created_at: str

class MistakeListResponse(BaseModel):
    user_id: str
    mistakes: List[MistakeRecord]
    total_count: int

# Strategy / Next Action
class StrategyNextResponse(BaseModel):
    user_id: str
    next_best_action: NextBestAction
    rationale: str
    focus_areas: List[str]

# Dream Company DNA
class DreamCompanyDNARequest(BaseModel):
    user_id: str
    company_name: str
    target_role: str

class DreamCompanyDNAResponse(BaseModel):
    company_name: str
    target_role: str
    matching_skills: List[str]
    missing_skills: List[str]
    weak_areas: List[str]
    recommended_preparation: List[str]
    assumptions_made: List[str]
