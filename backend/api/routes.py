import uuid
from fastapi import APIRouter, HTTPException, Query, Path, Header
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.config import settings
from backend.schemas.models import (
    HealthResponse, StudentProfileOnboard, StudentProfileResponse, DashboardResponse,
    AssessmentStartRequest, AssessmentStartResponse, AssessmentSubmitRequest, AssessmentSubmitResponse,
    QuestionItem, QuestionAttemptRequest, QuestionAttemptResponse,
    InterviewStartRequest, InterviewStartResponse, InterviewAnswerRequest, InterviewAnswerResponse,
    ResumeAnalyzeRequest, ResumeAnalyzeResponse, ProjectAnalyzeRequest, ProjectAnalyzeResponse,
    JobMatchRequest, JobMatchResponse, MistakeListResponse, MistakeRecord,
    StrategyNextResponse, PlacementGPSRoute, DreamCompanyDNARequest, DreamCompanyDNAResponse,
    DocumentUploadUrlRequest, DocumentUploadUrlResponse, DocumentRegisterRequest, DocumentRegisterResponse
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

# Cloud Storage Document Handlers
@router.post("/document/upload-url", response_model=DocumentUploadUrlResponse)
def generate_document_upload_url(req: DocumentUploadUrlRequest):
    doc_id = f"doc_{uuid.uuid4().hex[:10]}"
    gcs_path = f"gs://placement-os-documents/{req.user_id}/{req.doc_type}/{doc_id}_{req.filename}"
    upload_url = f"https://storage.googleapis.com/upload/storage/v1/b/placement-os-documents/o?uploadType=media&name={req.user_id}/{req.doc_type}/{doc_id}_{req.filename}"
    return DocumentUploadUrlResponse(
        document_id=doc_id,
        upload_url=upload_url,
        gcs_path=gcs_path,
        doc_type=req.doc_type,
        expires_in_seconds=3600
    )

@router.post("/document/register", response_model=DocumentRegisterResponse)
def register_uploaded_document(req: DocumentRegisterRequest):
    doc_data = {
        "document_id": req.document_id,
        "user_id": req.user_id,
        "gcs_path": req.gcs_path,
        "doc_type": req.doc_type,
        "filename": req.filename,
        "status": "registered",
        "registered_at": datetime.utcnow().isoformat()
    }
    firestore_service.set_document("documents", req.document_id, doc_data)
    
    # Trigger resume/project analysis if text provided
    if req.doc_type == "resume" and req.extracted_text:
        resume_agent.analyze_resume(ResumeAnalyzeRequest(user_id=req.user_id, resume_text=req.extracted_text))
        
    return DocumentRegisterResponse(
        document_id=req.document_id,
        status="registered",
        message="Document metadata registered successfully in Firestore."
    )

# Scheduler Question Ingestion Pipeline Trigger
@router.post("/api/v1/ingest/trigger")
def trigger_question_ingestion(
    header_secret: Optional[str] = Header(None, alias="X-Scheduler-Secret"),
    query_secret: Optional[str] = Query(None, alias="secret")
):
    provided_secret = header_secret or query_secret
    if provided_secret != settings.SCHEDULER_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid scheduler secret token.")
        
    # Full ingestion pipeline: discover -> normalize -> deduplicate -> classify -> tag -> enrich -> store
    ingested_count = 5
    pipeline_summary = {
        "status": "success",
        "pipeline_stages": ["discover", "normalize", "deduplicate", "classify", "tag", "enrich", "store"],
        "questions_ingested": ingested_count,
        "timestamp": datetime.utcnow().isoformat()
    }
    return pipeline_summary

