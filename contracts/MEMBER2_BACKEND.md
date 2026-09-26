# Integration Contract for Member 2 (FastAPI + Gemini AI)
**Owner:** Member 3 (Data Architecture & Question Intelligence)  
**Target:** Member 2 (FastAPI Backend & Gemini AI Engine)

---

## 1. Importing Models Directly

All Firestore schemas are standardized as Pydantic v2 models in `data_pipeline.models`. Member 2 can import them directly into FastAPI route signatures:

```python
from data_pipeline.models import (
    Question,
    QuestionAttempt,
    Mistake,
    StudentProfile,
    Assessment,
    Interview,
    Document,
    Event,
)
```

---

## 2. Ingestion Trigger Endpoint for Cloud Scheduler

To allow Member 4 (Cloud Scheduler) to trigger ingestion without re-implementing the pipeline, mount the ingestion runner inside your FastAPI application:

```python
from fastapi import APIRouter, Header, HTTPException, status
from data_pipeline.scheduler.ingestion_service import IngestionService

router = APIRouter(prefix="/api/v1/ingest", tags=["Ingestion"])
ingestion_service = IngestionService()

@router.post("/trigger")
async def trigger_ingestion(x_scheduler_secret: str = Header(None, alias="X-Scheduler-Secret")):
    if not ingestion_service.verify_auth_token(x_scheduler_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid scheduler authentication token."
        )
    
    summary = ingestion_service.run_ingestion_job(batch_limit=25)
    return summary
```

---

## 3. Pre-signed Upload URL Endpoint

Mount this endpoint to support frontend browser-to-GCS uploads:

```python
from fastapi import APIRouter, Depends, Query
from data_pipeline.storage.signed_urls import SignedUrlService

storage_router = APIRouter(prefix="/api/v1/storage", tags=["Storage"])
signed_url_svc = SignedUrlService()

@storage_router.get("/upload-url")
async def get_upload_url(
    doc_type: str = Query(..., regex="^(resume|project_report|presentation|readme)$"),
    filename: str = Query(...),
    student_id: str = Depends(get_current_authenticated_user_id)
):
    return signed_url_svc.generate_upload_signed_url(
        student_id=student_id,
        doc_type=doc_type,
        original_filename=filename,
    )
```

---

## 4. Question Evaluation & Mistake Logging Flow

When evaluating a student submission:
1. Fetch question from `questions/{question_id}`.
2. Evaluate submitted code using Gemini or test cases.
3. Write attempt to `question_attempts/{attempt_id}`:
   ```python
   attempt = QuestionAttempt(
       id=f"qa_{uuid.uuid4().hex[:12]}",
       student_id=student_id,
       question_id=question_id,
       status="PASSED" if score >= 80 else "FAILED",
       submitted_code_or_answer=code,
       score=score,
       feedback=gemini_feedback,
       attempted_at=datetime.now(timezone.utc).isoformat(),
   )
   db.collection("question_attempts").document(attempt.id).set(attempt.to_firestore_dict())
   ```
4. If submission failed or revealed a conceptual bug, log to `mistakes/{mistake_id}`:
   ```python
   mistake = Mistake(
       id=f"m_{uuid.uuid4().hex[:12]}",
       student_id=student_id,
       question_id=question_id,
       attempt_id=attempt.id,
       category=question.category,
       subcategory=question.subcategory,
       mistake_type="Logic", # Syntax, Logic, EdgeCase, TimeLimitExceeded, Conceptual
       ai_diagnosis=gemini_diagnosis,
       recommended_revision_date=(datetime.now(timezone.utc) + timedelta(days=3)).isoformat(),
   )
   db.collection("mistakes").document(mistake.id).set(mistake.to_firestore_dict())
   ```
5. Update `student_profiles/{student_id}` with incremental `readiness_score` and `category_progress`.
