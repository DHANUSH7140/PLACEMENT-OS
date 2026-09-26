"""
Realistic Seed Data for Student Collections.
Populates:
- users
- student_profiles
- assessments
- interviews
- question_attempts
- mistakes
- learning_plans
- documents
- events

Ensures Member 1's Lovable frontend and Member 2's FastAPI have rich, connected data out of the box.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone, timedelta

NOW = datetime.now(timezone.utc)
NOW_ISO = NOW.isoformat()
YESTERDAY_ISO = (NOW - timedelta(days=1)).isoformat()
TWO_DAYS_AGO = (NOW - timedelta(days=2)).isoformat()
FUTURE_DATE = (NOW + timedelta(days=45)).isoformat()

DEMO_STUDENT_ID = "usr_student_demo_01"

SEED_USERS: List[Dict[str, Any]] = [
    {
        "uid": DEMO_STUDENT_ID,
        "email": "alex.student@placementos.dev",
        "display_name": "Alex Mercer",
        "photo_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
        "role": "student",
        "created_at": TWO_DAYS_AGO,
        "last_login": NOW_ISO,
        "is_active": True,
    },
    {
        "uid": "usr_mentor_demo_02",
        "email": "sarah.mentor@placementos.dev",
        "display_name": "Sarah Jenkins",
        "photo_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah",
        "role": "mentor",
        "created_at": TWO_DAYS_AGO,
        "last_login": NOW_ISO,
        "is_active": True,
    }
]

SEED_STUDENT_PROFILES: List[Dict[str, Any]] = [
    {
        "student_id": DEMO_STUDENT_ID,
        "full_name": "Alex Mercer",
        "college_name": "National Institute of Technology",
        "branch": "Computer Science & Engineering",
        "graduation_year": 2026,
        "cgpa": 8.84,
        "target_companies": ["Amazon", "Google", "Microsoft", "Flipkart"],
        "target_roles": ["SDE-1", "Software Engineer"],
        "preferred_languages": ["Python", "Java", "C++"],
        "readiness_score": 76.5,
        "total_questions_solved": 48,
        "category_progress": {
            "DSA": 82.0,
            "SQL": 75.0,
            "DBMS": 85.0,
            "OS": 70.0,
            "Computer Networks": 65.0,
            "OOP": 90.0,
            "System Design": 55.0,
            "HR": 80.0
        },
        "strengths": ["Dynamic Programming", "OOP Design", "DBMS Transactions", "SQL Window Functions"],
        "weaknesses": ["Distributed System Design", "Network Subnetting", "Graph Traversal Edge Cases"],
        "resume_document_id": "doc_resume_alex_01",
        "active_learning_plan_id": "lp_sprint_60_alex",
        "created_at": TWO_DAYS_AGO,
        "updated_at": NOW_ISO,
    }
]

SEED_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "doc_resume_alex_01",
        "student_id": DEMO_STUDENT_ID,
        "document_type": "resume",
        "file_name": "alex_mercer_swe_resume.pdf",
        "mime_type": "application/pdf",
        "file_size_bytes": 184520,
        "gcs_bucket": "placement-os-documents.appspot.com",
        "gcs_blob_path": f"users/{DEMO_STUDENT_ID}/resumes/20260926_alex_mercer_swe_resume.pdf",
        "gcs_public_url": f"https://storage.googleapis.com/placement-os-documents.appspot.com/users/{DEMO_STUDENT_ID}/resumes/20260926_alex_mercer_swe_resume.pdf",
        "extracted_text_preview": "Alex Mercer | NIT CSE 2026 | Full Stack & Systems Engineering. Proficient in Python, Java, Docker, React, PostgreSQL. Built high-throughput microservices...",
        "extracted_skills": ["Python", "Java", "PostgreSQL", "Docker", "FastAPI", "React", "Data Structures"],
        "extracted_projects": ["Distributed Rate Limiting Gateway", "AI Resume Intelligence Engine"],
        "parsing_status": "PARSED",
        "created_at": TWO_DAYS_AGO,
        "updated_at": TWO_DAYS_AGO,
    },
    {
        "id": "doc_project_alex_02",
        "student_id": DEMO_STUDENT_ID,
        "document_type": "project_report",
        "file_name": "distributed_rate_limiter_report.pdf",
        "mime_type": "application/pdf",
        "file_size_bytes": 452100,
        "gcs_bucket": "placement-os-documents.appspot.com",
        "gcs_blob_path": f"users/{DEMO_STUDENT_ID}/project_reports/20260926_rate_limiter_report.pdf",
        "gcs_public_url": f"https://storage.googleapis.com/placement-os-documents.appspot.com/users/{DEMO_STUDENT_ID}/project_reports/20260926_rate_limiter_report.pdf",
        "extracted_text_preview": "Engineering Report: Low-latency distributed rate limiter using Redis Lua scripting and sliding window counter algorithm. Evaluated under 50k RPS...",
        "extracted_skills": ["Distributed Systems", "Redis", "Lua", "High Concurrency"],
        "extracted_projects": ["Distributed Rate Limiter"],
        "parsing_status": "PARSED",
        "created_at": YESTERDAY_ISO,
        "updated_at": YESTERDAY_ISO,
    }
]

SEED_LEARNING_PLANS: List[Dict[str, Any]] = [
    {
        "id": "lp_sprint_60_alex",
        "student_id": DEMO_STUDENT_ID,
        "title": "Amazon SDE-1 60-Day Placement Sprint",
        "target_company": "Amazon",
        "target_role": "SDE-1",
        "start_date": TWO_DAYS_AGO,
        "target_completion_date": FUTURE_DATE,
        "completion_percentage": 35.0,
        "status": "ACTIVE",
        "milestones": [
            {
                "milestone_id": "ms_01",
                "title": "Core DSA & Knapsack Patterns",
                "description": "Master 0/1 knapsack, unbounded knapsack, and subset sum patterns.",
                "due_date": (NOW + timedelta(days=7)).isoformat(),
                "is_completed": True,
                "tasks": [
                    {"task_id": "t1", "title": "Solve 0/1 Knapsack", "category": "DSA", "is_completed": True},
                    {"task_id": "t2", "title": "Solve Trapping Rain Water", "category": "DSA", "is_completed": True}
                ]
            },
            {
                "milestone_id": "ms_02",
                "title": "SQL & Transaction Concurrency",
                "description": "Master Window functions and ACID isolation levels.",
                "due_date": (NOW + timedelta(days=15)).isoformat(),
                "is_completed": False,
                "tasks": [
                    {"task_id": "t3", "title": "Solve Department Top Salaries in SQL", "category": "SQL", "is_completed": False},
                    {"task_id": "t4", "title": "Review ACID WAL Protocol", "category": "DBMS", "is_completed": True}
                ]
            }
        ],
        "created_at": TWO_DAYS_AGO,
        "updated_at": NOW_ISO,
    }
]

SEED_ASSESSMENTS: List[Dict[str, Any]] = [
    {
        "id": "asm_amazon_mock_01",
        "student_id": DEMO_STUDENT_ID,
        "title": "Amazon SDE-1 Comprehensive Mock Diagnostic",
        "assessment_type": "COMPANY_MOCK",
        "company": "Amazon",
        "role": "SDE-1",
        "question_ids": ["q_01knapsack", "q_trappingrain", "q_sqltop3"],
        "time_limit_minutes": 90,
        "status": "COMPLETED",
        "score": 85.0,
        "total_questions": 3,
        "passed_questions": 2,
        "category_scores": {"DSA": 88.0, "SQL": 80.0},
        "feedback": "Strong algorithmic formulation on 0/1 Knapsack. SQL query had minor edge case regarding departments with fewer than 3 employees.",
        "started_at": YESTERDAY_ISO,
        "completed_at": YESTERDAY_ISO,
        "created_at": TWO_DAYS_AGO,
    }
]

SEED_INTERVIEWS: List[Dict[str, Any]] = [
    {
        "id": "intv_alex_mock_01",
        "student_id": DEMO_STUDENT_ID,
        "interview_type": "TECHNICAL",
        "target_company": "Amazon",
        "target_role": "SDE-1",
        "status": "COMPLETED",
        "duration_minutes": 45,
        "turns": [
            {
                "speaker": "ai_interviewer",
                "message": "Welcome Alex! Let's start with your technical background and then solve a dynamic programming challenge.",
                "timestamp": YESTERDAY_ISO
            },
            {
                "speaker": "student",
                "message": "Hi! I'm a final-year CS undergrad focusing on high-performance distributed systems. Looking forward to the problem.",
                "timestamp": YESTERDAY_ISO
            },
            {
                "speaker": "ai_interviewer",
                "message": "Great. Could you walk me through the 0/1 Knapsack problem and state your recurrence relation?",
                "timestamp": YESTERDAY_ISO
            },
            {
                "speaker": "student",
                "message": "Sure. At each item i with weight wt[i] and value val[i], we either include it or exclude it. dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]]).",
                "timestamp": YESTERDAY_ISO
            }
        ],
        "rubric_scores": {
            "problem_solving": 8.5,
            "technical_depth": 8.0,
            "communication": 9.0,
            "system_architecture": 7.0,
            "culture_fit": 8.5
        },
        "overall_score": 82.5,
        "strengths_identified": ["Clear articulation of DP states", "Prompt edge-case identification"],
        "areas_for_improvement": ["Elaborate on space-optimization earlier in the discussion"],
        "detailed_feedback": "Excellent performance overall. Candidate clearly explained the DP recurrence and reduced space complexity from O(NW) to O(W).",
        "started_at": YESTERDAY_ISO,
        "completed_at": YESTERDAY_ISO,
        "created_at": YESTERDAY_ISO,
    }
]

SEED_QUESTION_ATTEMPTS: List[Dict[str, Any]] = [
    {
        "id": "qa_alex_attempt_01",
        "student_id": DEMO_STUDENT_ID,
        "question_id": "q_01knapsack",
        "assessment_id": "asm_amazon_mock_01",
        "status": "PASSED",
        "submitted_code_or_answer": "def knapSack(W, wt, val, n):\n    dp = [0] * (W + 1)\n    for i in range(n):\n        for w in range(W, wt[i] - 1, -1):\n            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])\n    return dp[W]",
        "language": "python",
        "execution_time_ms": 42.5,
        "memory_used_kb": 14200.0,
        "score": 100.0,
        "feedback": "All test cases passed. Excellent space-optimized O(W) implementation.",
        "time_taken_seconds": 920,
        "attempted_at": YESTERDAY_ISO,
    }
]

SEED_MISTAKES: List[Dict[str, Any]] = [
    {
        "id": "m_alex_01",
        "student_id": DEMO_STUDENT_ID,
        "question_id": "q_sqltop3",
        "attempt_id": "qa_alex_attempt_02",
        "category": "SQL",
        "subcategory": "Window Functions",
        "mistake_type": "EdgeCase",
        "student_notes": "Forgot that departments with tied salaries or fewer than 3 employees might cause NULL ranks.",
        "ai_diagnosis": "Use DENSE_RANK() instead of RANK() to avoid skipping rank values when ties exist.",
        "recommended_revision_date": (NOW + timedelta(days=3)).isoformat(),
        "is_resolved": False,
        "created_at": YESTERDAY_ISO,
    }
]

SEED_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "evt_01",
        "student_id": DEMO_STUDENT_ID,
        "event_type": "LOGIN",
        "payload": {"ip": "127.0.0.1", "device": "Chrome Windows"},
        "timestamp": TWO_DAYS_AGO,
    },
    {
        "id": "evt_02",
        "student_id": DEMO_STUDENT_ID,
        "event_type": "ASSESSMENT_COMPLETE",
        "payload": {"assessment_id": "asm_amazon_mock_01", "score": 85.0},
        "timestamp": YESTERDAY_ISO,
    }
]
