# PLACEMENT OS — Canonical Firestore Schema Reference
**Owner:** Member 3 (Data Architecture & Question Intelligence)  
**Target Audience:** Member 1 (Frontend), Member 2 (Backend), Member 4 (Cloud & BigQuery)

---

## 1. Overview of Collections

PLACEMENT OS uses a single, consistent, multi-tenant Firestore architecture organized into **10 core collections**:

| Collection | Scope | Access Model | Primary Document Key | Description |
|---|---|---|---|---|
| `questions` | Public/Shared | Authenticated Read, Admin Write | `q_{hash[:16]}` | Master question bank across 26 canonical taxonomies. |
| `users` | Private/System | Owner Read/Write, Admin Full | `uid` (Firebase Auth) | Core authentication identities and roles. |
| `student_profiles` | Private | Owner Read/Write, Mentor Read | `student_id` (matches `uid`) | Academic, readiness score, target companies/roles. |
| `question_attempts` | Private | Owner Read/Create, Admin Full | `qa_{uuid}` | Code/answer submissions, test results, scores. |
| `assessments` | Private | Owner Read/Write, Mentor Read | `asm_{uuid}` | Diagnostic and mock tests with question sets. |
| `interviews` | Private | Owner Read/Write, Mentor Read | `intv_{uuid}` | AI mock interview transcripts and rubric scores. |
| `mistakes` | Private | Owner Read/Write | `m_{uuid}` | Personalized error log and spaced-repetition revision. |
| `learning_plans` | Private | Owner Read/Write | `lp_{uuid}` | 30-90 day milestone sprints and daily tasks. |
| `documents` | Private | Owner Read/Write | `doc_{uuid}` | Metadata & GCS pointers for Resumes, PPTs, READMEs. |
| `events` | Private/Telemetry | Owner Create, Admin Read | `evt_{uuid}` | Activity telemetry and event streaming. |

---

## 2. Detailed Collection Schemas

### 2.1. `questions` Collection
```json
{
  "id": "q_77e6ca2d0bcbf56b",
  "category": "DSA",
  "subcategory": "Dynamic Programming",
  "topic": "Knapsack",
  "skills": ["Dynamic Programming", "0/1 Knapsack", "Recursion", "Memoization"],
  "question_type": "Coding",
  "difficulty": "Medium",
  "companies": ["Google", "Amazon", "Microsoft", "Flipkart"],
  "roles": ["SDE-1", "Software Engineer"],
  "observed_frequency": 14,
  "source_count": 4,
  "first_seen": "2026-09-01T12:00:00Z",
  "last_seen": "2026-09-26T10:30:00Z",
  "student_relevance": 0.88,
  "title": "0/1 Knapsack Problem",
  "problem_statement": "Given weights and values of N items, put these items in a knapsack...",
  "explanation": "Core concept involves binary choices: include item or exclude item.",
  "options": null,
  "correct_answer": null,
  "solution_approach": "Use 2D or 1D Dynamic Programming...",
  "code_snippets": {
    "python": "def knapSack(W, wt, val, n):\n    # implementation\n    pass"
  },
  "test_cases": [
    {
      "input": "W = 4, val = [1, 2, 3], wt = [4, 5, 1]",
      "expected_output": "3",
      "is_hidden": false,
      "explanation": "Pick item 3 with wt=1 and val=3."
    }
  ],
  "learning_hints": [
    "Consider the binary choice for each item: include it or exclude it.",
    "If you include an item, what happens to the remaining knapsack capacity?"
  ],
  "content_hash": "77e6ca2d0bcbf56b...",
  "sources": [
    {
      "source_name": "open_placement_benchmark",
      "source_url": "https://open-curriculum.edu/questions/dp_knap_01",
      "source_item_id": "dp_knap_01",
      "discovered_at": "2026-09-01T12:00:00Z",
      "attribution": "Discovered via open_placement_benchmark"
    }
  ],
  "is_active": true,
  "created_at": "2026-09-01T12:00:00Z",
  "updated_at": "2026-09-26T10:30:00Z"
}
```

> [!NOTE]
> **Reporting Rule:** Always display `observed_frequency` and `source_count`. Never claim absolute market frequency on the frontend or backend.

---

### 2.2. `student_profiles` Collection
```json
{
  "student_id": "usr_student_demo_01",
  "full_name": "Alex Mercer",
  "college_name": "National Institute of Technology",
  "branch": "Computer Science & Engineering",
  "graduation_year": 2026,
  "cgpa": 8.84,
  "target_companies": ["Amazon", "Google", "Microsoft"],
  "target_roles": ["SDE-1", "Software Engineer"],
  "preferred_languages": ["Python", "Java"],
  "readiness_score": 76.5,
  "total_questions_solved": 48,
  "category_progress": {
    "DSA": 82.0,
    "SQL": 75.0,
    "OS": 70.0
  },
  "strengths": ["Dynamic Programming", "SQL Window Functions"],
  "weaknesses": ["Distributed System Design", "Network Subnetting"],
  "resume_document_id": "doc_resume_alex_01",
  "active_learning_plan_id": "lp_sprint_60_alex",
  "created_at": "2026-09-24T00:00:00Z",
  "updated_at": "2026-09-26T10:00:00Z"
}
```

---

### 2.3. `documents` Collection (Cloud Storage Pointers)
```json
{
  "id": "doc_resume_alex_01",
  "student_id": "usr_student_demo_01",
  "document_type": "resume",
  "file_name": "alex_mercer_swe_resume.pdf",
  "mime_type": "application/pdf",
  "file_size_bytes": 184520,
  "gcs_bucket": "placement-os-documents.appspot.com",
  "gcs_blob_path": "users/usr_student_demo_01/resumes/20260926_resume.pdf",
  "gcs_public_url": "https://storage.googleapis.com/placement-os-documents.appspot.com/users/...",
  "extracted_text_preview": "Alex Mercer | NIT CSE 2026...",
  "extracted_skills": ["Python", "Java", "Docker", "PostgreSQL"],
  "extracted_projects": ["Distributed Rate Limiter"],
  "parsing_status": "PARSED",
  "created_at": "2026-09-24T00:00:00Z",
  "updated_at": "2026-09-24T00:00:00Z"
}
```

---

### 2.4. `question_attempts` Collection
```json
{
  "id": "qa_attempt_01",
  "student_id": "usr_student_demo_01",
  "question_id": "q_77e6ca2d0bcbf56b",
  "assessment_id": "asm_amazon_mock_01",
  "status": "PASSED",
  "submitted_code_or_answer": "def knapSack(W, wt, val, n): ...",
  "language": "python",
  "execution_time_ms": 42.5,
  "memory_used_kb": 14200.0,
  "score": 100.0,
  "feedback": "All test cases passed. Optimal space complexity.",
  "time_taken_seconds": 920,
  "attempted_at": "2026-09-25T14:30:00Z"
}
```

---

### 2.5. `mistakes` Collection
```json
{
  "id": "m_alex_01",
  "student_id": "usr_student_demo_01",
  "question_id": "q_sqltop3",
  "attempt_id": "qa_alex_attempt_02",
  "category": "SQL",
  "subcategory": "Window Functions",
  "mistake_type": "EdgeCase",
  "student_notes": "Forgot that departments with fewer than 3 employees return fewer rows.",
  "ai_diagnosis": "Use DENSE_RANK() instead of RANK() to avoid skipping rank values.",
  "recommended_revision_date": "2026-09-29T00:00:00Z",
  "is_resolved": false,
  "created_at": "2026-09-25T15:00:00Z"
}
```

---

### 2.6. `learning_plans` Collection
```json
{
  "id": "lp_sprint_60_alex",
  "student_id": "usr_student_demo_01",
  "title": "Amazon SDE-1 60-Day Placement Sprint",
  "target_company": "Amazon",
  "target_role": "SDE-1",
  "start_date": "2026-09-24T00:00:00Z",
  "target_completion_date": "2026-11-24T00:00:00Z",
  "completion_percentage": 35.0,
  "status": "ACTIVE",
  "milestones": [
    {
      "milestone_id": "ms_01",
      "title": "Core DSA & Knapsack Patterns",
      "description": "Master 0/1 knapsack, unbounded knapsack, and subset sum.",
      "due_date": "2026-10-01T00:00:00Z",
      "is_completed": true,
      "tasks": [
        {"task_id": "t1", "title": "Solve 0/1 Knapsack", "category": "DSA", "is_completed": true}
      ]
    }
  ],
  "created_at": "2026-09-24T00:00:00Z",
  "updated_at": "2026-09-26T10:00:00Z"
}
```

---

### 2.7. `assessments` Collection
```json
{
  "id": "asm_amazon_mock_01",
  "student_id": "usr_student_demo_01",
  "title": "Amazon SDE-1 Comprehensive Mock Diagnostic",
  "assessment_type": "COMPANY_MOCK",
  "company": "Amazon",
  "role": "SDE-1",
  "question_ids": ["q_77e6ca2d0bcbf56b", "q_trappingrain"],
  "time_limit_minutes": 90,
  "status": "COMPLETED",
  "score": 85.0,
  "total_questions": 2,
  "passed_questions": 2,
  "category_scores": {"DSA": 88.0},
  "feedback": "Strong algorithmic formulation.",
  "started_at": "2026-09-25T14:00:00Z",
  "completed_at": "2026-09-25T15:30:00Z",
  "created_at": "2026-09-24T00:00:00Z"
}
```

---

### 2.8. `interviews` Collection
```json
{
  "id": "intv_alex_mock_01",
  "student_id": "usr_student_demo_01",
  "interview_type": "TECHNICAL",
  "target_company": "Amazon",
  "target_role": "SDE-1",
  "status": "COMPLETED",
  "duration_minutes": 45,
  "turns": [
    {"speaker": "ai_interviewer", "message": "Welcome Alex! Let's solve a DP challenge."},
    {"speaker": "student", "message": "Sure, I'm ready."}
  ],
  "rubric_scores": {
    "problem_solving": 8.5,
    "technical_depth": 8.0,
    "communication": 9.0,
    "system_architecture": 7.0,
    "culture_fit": 8.5
  },
  "overall_score": 82.5,
  "strengths_identified": ["Clear articulation of DP states"],
  "areas_for_improvement": ["Elaborate on space-optimization earlier"],
  "detailed_feedback": "Excellent performance overall.",
  "started_at": "2026-09-25T16:00:00Z",
  "completed_at": "2026-09-25T16:45:00Z",
  "created_at": "2026-09-25T15:55:00Z"
}
```

---

### 2.9. `events` Collection
```json
{
  "id": "evt_02",
  "student_id": "usr_student_demo_01",
  "event_type": "ASSESSMENT_COMPLETE",
  "session_id": "sess_abc123",
  "payload": {"assessment_id": "asm_amazon_mock_01", "score": 85.0},
  "timestamp": "2026-09-25T15:30:00Z"
}
```

---

### 2.10. `users` Collection
```json
{
  "uid": "usr_student_demo_01",
  "email": "alex.student@placementos.dev",
  "display_name": "Alex Mercer",
  "photo_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
  "role": "student",
  "created_at": "2026-09-24T00:00:00Z",
  "last_login": "2026-09-26T10:00:00Z",
  "is_active": true
}
```
