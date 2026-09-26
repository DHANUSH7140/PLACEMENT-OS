"""
Unit Tests for Placement OS Firestore Data Models.
"""

import pytest
from data_pipeline.models.question import Question, QuestionAttempt, Mistake, TestCase, QuestionSource
from data_pipeline.models.student import User, StudentProfile, LearningPlan, Event
from data_pipeline.models.assessment import Assessment, Interview, InterviewTurn
from data_pipeline.models.document import Document


def test_question_model_schema():
    q = Question(
        id="q_sample_01",
        category="DSA",
        subcategory="Dynamic Programming",
        topic="Knapsack",
        skills=["Dynamic Programming", "0/1 Knapsack", "Recursion", "Memoization"],
        question_type="Coding",
        difficulty="Medium",
        companies=["Google", "Amazon"],
        roles=["SDE-1"],
        observed_frequency=12,
        source_count=3,
        first_seen="2026-09-01T00:00:00Z",
        last_seen="2026-09-26T00:00:00Z",
        student_relevance=0.88,
        title="0/1 Knapsack Problem",
        problem_statement="Given weights and values...",
        content_hash="abc123hash",
    )
    d = q.to_firestore_dict()
    assert d["id"] == "q_sample_01"
    assert d["category"] == "DSA"
    assert d["observed_frequency"] == 12
    assert d["source_count"] == 3
    assert len(d["skills"]) == 4
    assert "Google" in d["companies"]


def test_student_profile_schema():
    sp = StudentProfile(
        student_id="usr_test_01",
        full_name="Jane Doe",
        target_companies=["Amazon", "Microsoft"],
        readiness_score=82.0,
    )
    d = sp.to_firestore_dict()
    assert d["student_id"] == "usr_test_01"
    assert d["readiness_score"] == 82.0
    assert "Amazon" in d["target_companies"]


def test_document_model_schema():
    doc = Document(
        id="doc_test_01",
        student_id="usr_test_01",
        document_type="resume",
        file_name="resume.pdf",
        mime_type="application/pdf",
        file_size_bytes=102400,
        gcs_bucket="test-bucket",
        gcs_blob_path="users/usr_test_01/resumes/resume.pdf",
    )
    d = doc.to_firestore_dict()
    assert d["document_type"] == "resume"
    assert d["parsing_status"] == "UPLOADED"
    assert d["file_size_bytes"] == 102400
