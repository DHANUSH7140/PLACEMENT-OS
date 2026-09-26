from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.schemas.models import (
    HealthResponse, StudentProfileOnboard, StudentProfileResponse, DashboardResponse,
    AssessmentStartRequest, AssessmentStartResponse, AssessmentSubmitRequest, AssessmentSubmitResponse,
    QuestionItem, QuestionAttemptRequest, QuestionAttemptResponse,
    InterviewStartRequest, InterviewStartResponse, InterviewAnswerRequest, InterviewAnswerResponse,
    ResumeAnalyzeRequest, ResumeAnalyzeResponse, ProjectAnalyzeRequest, ProjectAnalyzeResponse,
    JobMatchRequest, JobMatchResponse, MistakeListResponse, MistakeRecord,
    StrategyNextResponse, PlacementGPSRoute, DreamCompanyDNARequest, DreamCompanyDNAResponse
)
from backend.services.firestore_service import firestore_service
from backend.agents.profile.profile_agent import profile_agent
from backend.agents.assessment.assessment_agent import assessment_agent
from backend.agents.skill_gap.skill_gap_agent import skill_gap_agent
from backend.agents.personalization.personalization_agent import personalization_agent
from backend.agents.interview.interview_agent import interview_agent
from backend.agents.resume.resume_agent import resume_agent
from backend.agents.strategy.strategy_agent import strategy_agent

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        version="1.0.0",
        services={
            "fastapi": "healthy",
            "firestore": "connected" if firestore_service.db else "in_memory_fallback",
            "gemini": "configured"
        }
    )

@router.post("/profile/onboard", response_model=StudentProfileResponse)
def onboard_student(req: StudentProfileOnboard):
    return profile_agent.onboard_student(req)

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(user_id: str = Query(..., description="Student User ID")):
    profile = firestore_service.get_document("student_profiles", user_id)
    if not profile:
        # Auto onboard default user if not found for easy frontend integration
        profile_res = profile_agent.onboard_student(StudentProfileOnboard(
            user_id=user_id,
            name="Student",
            email=f"{user_id}@example.com",
            target_role="Backend Engineer",
            target_company="Tier 1 Product Company"
        ))
        profile = profile_res.model_dump()

    placement_route = strategy_agent.get_placement_route(user_id)
    mistakes = firestore_service.query_collection("mistakes", "user_id", user_id)
    
    return DashboardResponse(
        user_id=user_id,
        student_name=profile.get("name", "Student"),
        target_role=profile.get("target_role", "Backend Engineer"),
        target_company=profile.get("target_company", "Tier 1 Product Company"),
        readiness=profile.get("readiness"),
        placement_route=placement_route,
        active_missions=[
            {
                "mission_id": "m_1",
                "title": "Complete BFS/DFS Graph Module",
                "status": "in_progress",
                "progress_percentage": 40
            }
        ],
        recent_mistakes_count=len(mistakes)
    )

@router.post("/assessment/start", response_model=AssessmentStartResponse)
def start_assessment(req: AssessmentStartRequest):
    return assessment_agent.start_assessment(req)

@router.post("/assessment/{assessment_id}/submit", response_model=AssessmentSubmitResponse)
def submit_assessment(assessment_id: str, req: AssessmentSubmitRequest):
    return assessment_agent.submit_assessment(assessment_id, req)

@router.get("/questions", response_model=List[QuestionItem])
def get_questions(
    category: Optional[str] = Query(None, description="Question category filter (DSA, Aptitude, SQL, CS Fundamentals)"),
    difficulty: Optional[str] = Query(None, description="Difficulty filter (Easy, Medium, Hard)")
):
    return assessment_agent.get_questions(category=category, difficulty=difficulty)

@router.post("/questions/{question_id}/attempt", response_model=QuestionAttemptResponse)
def attempt_question(question_id: str, req: QuestionAttemptRequest):
    req.question_id = question_id
    return assessment_agent.record_question_attempt(req)

@router.post("/interview/start", response_model=InterviewStartResponse)
def start_interview(req: InterviewStartRequest):
    return interview_agent.start_interview(req)

@router.post("/interview/{interview_id}/answer", response_model=InterviewAnswerResponse)
def answer_interview(interview_id: str, req: InterviewAnswerRequest):
    return interview_agent.answer_interview_question(interview_id, req)

@router.post("/resume/analyze", response_model=ResumeAnalyzeResponse)
def analyze_resume(req: ResumeAnalyzeRequest):
    return resume_agent.analyze_resume(req)

@router.post("/project/analyze", response_model=ProjectAnalyzeResponse)
def analyze_project(req: ProjectAnalyzeRequest):
    return resume_agent.analyze_project(req)

@router.post("/resume/job-match", response_model=JobMatchResponse)
def match_job(req: JobMatchRequest):
    return resume_agent.match_job(req)

@router.get("/mistakes", response_model=MistakeListResponse)
def get_mistakes(user_id: str = Query(..., description="Student User ID")):
    records = firestore_service.query_collection("mistakes", "user_id", user_id)
    mistake_objs = [MistakeRecord(**r) for r in records]
    return MistakeListResponse(
        user_id=user_id,
        mistakes=mistake_objs,
        total_count=len(mistake_objs)
    )

@router.get("/strategy/next", response_model=StrategyNextResponse)
def get_next_strategy(user_id: str = Query(..., description="Student User ID")):
    return strategy_agent.get_next_action(user_id)

@router.get("/placement-route", response_model=PlacementGPSRoute)
def get_placement_route(
    user_id: str = Query(..., description="Student User ID"),
    recalculate: bool = Query(False, description="Force AI route recalculation")
):
    return strategy_agent.get_placement_route(user_id, force_recalculate=recalculate)

@router.post("/strategy/dream-company-dna", response_model=DreamCompanyDNAResponse)
def get_dream_company_dna(req: DreamCompanyDNARequest):
    return strategy_agent.get_dream_company_dna(req)
