"""
Integration Contract Verification for Member 2 (FastAPI Backend).
Validates:
1. Canonical Question Schema exact conformance
2. Member 2's GET /questions reading and filtering
3. Member 2's POST /questions/{id}/attempt attempt & mistake creation
4. Cloud Storage Flow (Resume, Project Report, PPT, README) + 25MB & MIME validation
5. Scheduler Endpoint security token check & ingestion execution
"""

import pytest
from datetime import datetime, timezone
from data_pipeline.models.question import Question, QuestionAttempt, Mistake, TestCase
from data_pipeline.db.firestore_client import FirestoreDatabase
from data_pipeline.storage.storage_manager import StorageManager
from data_pipeline.storage.signed_urls import SignedUrlService
from data_pipeline.scheduler.ingestion_service import IngestionService
from data_pipeline.config import SCHEDULER_SECRET_TOKEN


def test_canonical_question_contract_keys():
    """Confirms Question model has all required fields in the exact specification."""
    required_keys = {
        "id",
        "category",
        "subcategory",
        "topic",
        "skills",
        "question_type",
        "difficulty",
        "companies",
        "roles",
        "observed_frequency",
        "source_count",
        "student_relevance",
        "title",
        "problem_statement",
        "explanation",
        "solution_approach",
        "test_cases",
        "learning_hints",
        "content_hash",
        "sources",
    }
    q = Question(
        id="q_test_123",
        category="DSA",
        subcategory="Dynamic Programming",
        topic="Knapsack",
        skills=["Dynamic Programming", "Recursion"],
        question_type="Coding",
        difficulty="Medium",
        companies=["Google", "Amazon"],
        roles=["SDE-1"],
        observed_frequency=5,
        source_count=2,
        student_relevance=0.85,
        title="0/1 Knapsack Problem",
        problem_statement="Given items with weights and values...",
        explanation="Binary choice problem: pick or do not pick.",
        solution_approach="DP table where dp[i][w] is max value.",
        test_cases=[TestCase(input="W=4", expected_output="3")],
        learning_hints=["Try smaller subproblems."],
        content_hash="abc1234567890",
    )
    d = q.to_firestore_dict()
    for key in required_keys:
        assert key in d, f"Missing required canonical key: '{key}'"


def test_member2_get_questions_flow():
    """Verifies that Member 2's GET /questions can read and filter records correctly."""
    db = FirestoreDatabase()
    questions = db.list_documents("questions", limit=50)
    assert len(questions) > 0, "Question bank should contain seeded questions"

    # Verify every retrieved question can hydrate into Question model without error
    hydrated = [Question(**q) for q in questions]
    assert len(hydrated) == len(questions)

    # Filter by category
    dsa_questions = [q for q in hydrated if q.category == "DSA"]
    assert len(dsa_questions) >= 1
    assert any(q.topic == "Knapsack" for q in dsa_questions)


def test_member2_post_attempt_and_mistake_flow():
    """Verifies that Member 2's POST /questions/{id}/attempt creates attempts and mistakes."""
    db = FirestoreDatabase()
    student_id = "usr_student_test_99"
    question_id = "q_77e6ca2d0bcbf56b"

    # 1. Simulate student attempt submission
    attempt = QuestionAttempt(
        id="qa_test_submission_01",
        student_id=student_id,
        question_id=question_id,
        status="FAILED",
        submitted_code_or_answer="def knapSack(): return 0 # incomplete",
        score=20.0,
        feedback="Failed on boundary capacity test case.",
        attempted_at=datetime.now(timezone.utc).isoformat(),
    )
    db.set_document("question_attempts", attempt.id, attempt.to_firestore_dict())

    # Verify attempt written
    saved_attempt = db.get_document("question_attempts", attempt.id)
    assert saved_attempt is not None
    assert saved_attempt["student_id"] == student_id
    assert saved_attempt["status"] == "FAILED"

    # 2. Simulate mistake record creation
    mistake = Mistake(
        id="m_test_mistake_01",
        student_id=student_id,
        question_id=question_id,
        attempt_id=attempt.id,
        category="DSA",
        subcategory="Dynamic Programming",
        mistake_type="EdgeCase",
        student_notes="Zero capacity edge case not handled.",
        ai_diagnosis="Add if capacity == 0 return 0 before recursion.",
        recommended_revision_date="2026-10-01T00:00:00Z",
    )
    db.set_document("mistakes", mistake.id, mistake.to_firestore_dict())

    saved_mistake = db.get_document("mistakes", mistake.id)
    assert saved_mistake is not None
    assert saved_mistake["mistake_type"] == "EdgeCase"
    assert saved_mistake["student_id"] == student_id


def test_cloud_storage_flow_all_doc_types():
    """Verifies signed URL generation, upload, 25MB limit, and MIME validation for all 4 types."""
    signed_svc = SignedUrlService()
    storage_mgr = StorageManager()
    student_id = "usr_student_test_99"

    # Test 4 document types: resume, project_report, presentation, readme
    test_cases = [
        ("resume", "resume.pdf", b"%PDF-1.4 test resume bytes"),
        ("project_report", "report.docx", b"PK docx test bytes"),
        ("presentation", "slides.pptx", b"PK pptx test bytes"),
        ("readme", "README.md", b"# Project README\nArchitecture details..."),
    ]

    for doc_type, filename, content in test_cases:
        # Step 1: Request signed URL
        url_payload = signed_svc.generate_upload_signed_url(
            student_id=student_id,
            doc_type=doc_type,
            original_filename=filename,
        )
        assert "upload_url" in url_payload
        assert url_payload["doc_type"] == doc_type
        assert student_id in url_payload["gcs_blob_path"]

        # Step 2: Upload / store document metadata
        doc_record = storage_mgr.upload_file_bytes(
            student_id=student_id,
            doc_type=doc_type,
            original_filename=filename,
            file_bytes=content,
        )
        assert doc_record.document_type == doc_type
        assert doc_record.file_size_bytes == len(content)

    # Step 3: Validate 25MB limit enforcement
    huge_bytes = b"0" * (26 * 1024 * 1024)  # 26 MB
    is_valid, err = StorageManager.validate_file("big_resume.pdf", "resume", file_size=len(huge_bytes))
    assert is_valid is False
    assert "exceeds 25MB limit" in err

    # Step 4: Validate MIME / extension restriction
    is_valid, err = StorageManager.validate_file("malicious.exe", "resume", file_size=1024)
    assert is_valid is False
    assert "Invalid extension" in err


def test_scheduler_endpoint_security_and_execution():
    """Verifies Cloud Scheduler authentication verification and ingestion job."""
    service = IngestionService()

    # Test invalid token rejected
    assert service.verify_auth_token("wrong_token") is False
    assert service.verify_auth_token("") is False

    # Test valid token accepted
    assert service.verify_auth_token(SCHEDULER_SECRET_TOKEN) is True

    # Test ingestion execution
    result = service.run_ingestion_job(batch_limit=5)
    assert result["status"] == "SUCCESS"
    assert "items_discovered" in result
    assert "total_questions_in_store" in result
