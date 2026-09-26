import pytest
import httpx
from backend.main import app

@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.anyio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "fastapi" in data["services"]

@pytest.mark.anyio
async def test_student_onboarding(client):
    payload = {
        "user_id": "test_user_101",
        "name": "Alex Mercer",
        "email": "alex@example.com",
        "target_role": "Backend Engineer",
        "target_company": "Google",
        "preparation_weeks": 12,
        "known_skills": ["Python", "SQL"]
    }
    response = await client.post("/profile/onboard", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_101"
    assert data["readiness"]["overall_score"] > 0
    assert "aptitude" in data["readiness"]["dimensions"]

@pytest.mark.anyio
async def test_dashboard(client):
    response = await client.get("/dashboard?user_id=test_user_101")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_101"
    assert data["target_role"] == "Backend Engineer"
    assert "placement_route" in data

@pytest.mark.anyio
async def test_questions_and_attempt(client):
    # Fetch questions
    q_resp = await client.get("/questions?category=DSA")
    assert q_resp.status_code == 200
    questions = q_resp.json()
    assert len(questions) > 0
    
    q_id = questions[0]["question_id"]
    
    # Attempt question
    attempt_payload = {
        "user_id": "test_user_101",
        "question_id": q_id,
        "submitted_answer": "Queue (BFS)",
        "time_taken_seconds": 25
    }
    att_resp = await client.post(f"/questions/{q_id}/attempt", json=attempt_payload)
    assert att_resp.status_code == 200
    att_data = att_resp.json()
    assert att_data["user_id"] == "test_user_101"
    assert "is_correct" in att_data

@pytest.mark.anyio
async def test_assessment_flow(client):
    start_payload = {
        "user_id": "test_user_101",
        "category": "DSA",
        "question_count": 2
    }
    start_res = await client.post("/assessment/start", json=start_payload)
    assert start_res.status_code == 200
    asm_data = start_res.json()
    asm_id = asm_data["assessment_id"]
    
    # Submit assessment
    submit_payload = {
        "user_id": "test_user_101",
        "answers": [
            {
                "question_id": asm_data["questions"][0]["question_id"],
                "submitted_answer": "Wrong Answer",
                "time_taken_seconds": 30
            }
        ]
    }
    sub_res = await client.post(f"/assessment/{asm_id}/submit", json=submit_payload)
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert sub_data["assessment_id"] == asm_id
    assert "overall_score" in sub_data

@pytest.mark.anyio
async def test_mistakes_retrieval(client):
    response = await client.get("/mistakes?user_id=test_user_101")
    assert response.status_code == 200
    data = response.json()
    assert "total_count" in data

@pytest.mark.anyio
async def test_interview_flow(client):
    start_payload = {
        "user_id": "test_user_101",
        "interview_type": "technical",
        "target_role": "Backend Engineer",
        "target_company": "Amazon"
    }
    start_res = await client.post("/interview/start", json=start_payload)
    assert start_res.status_code == 200
    int_data = start_res.json()
    int_id = int_data["interview_id"]
    assert "question" in int_data
    
    # Answer interview question
    ans_payload = {
        "user_id": "test_user_101",
        "candidate_answer": "I would use a hash map to achieve O(1) lookup time complexity."
    }
    ans_res = await client.post(f"/interview/{int_id}/answer", json=ans_payload)
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert "evaluation" in ans_data
    assert "overall_answer_score" in ans_data["evaluation"]

@pytest.mark.anyio
async def test_resume_analysis(client):
    resume_text = """
    Jane Doe - Software Engineer
    Skills: Python, FastAPI, PostgreSQL, Docker, Redis
    Project: E-Commerce Platform
    Built RESTful microservices for payment processing using FastAPI and Docker.
    """
    response = await client.post("/resume/analyze", json={"user_id": "test_user_101", "resume_text": resume_text})
    assert response.status_code == 200
    data = response.json()
    assert "Python" in data["extracted_skills"]
    assert len(data["resume_grounded_questions"]) > 0

@pytest.mark.anyio
async def test_project_analysis(client):
    payload = {
        "user_id": "test_user_101",
        "project_title": "Placement OS",
        "project_description": "AI powered placement preparation engine built with FastAPI and Gemini.",
        "tech_stack": ["Python", "FastAPI", "Gemini", "Firestore"]
    }
    response = await client.post("/project/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["complexity_score"] > 0
    assert len(data["potential_interview_questions"]) > 0

@pytest.mark.anyio
async def test_job_match(client):
    payload = {
        "user_id": "test_user_101",
        "resume_text": "Python FastAPI developer with 2 years of backend experience.",
        "job_description": "Looking for a Backend Developer skilled in Python, FastAPI, and Kubernetes."
    }
    response = await client.post("/resume/job-match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["match_score"] > 0
    assert "Kubernetes" in data["missing_skills"]

@pytest.mark.anyio
async def test_placement_route_recalculation(client):
    response = await client.get("/placement-route?user_id=test_user_101&recalculate=true")
    assert response.status_code == 200
    data = response.json()
    assert data["route_status"] in ["on_track", "recalculated"]
    assert len(data["route"]) > 0

@pytest.mark.anyio
async def test_strategy_next(client):
    response = await client.get("/strategy/next?user_id=test_user_101")
    assert response.status_code == 200
    data = response.json()
    assert "next_best_action" in data

@pytest.mark.anyio
async def test_dream_company_dna(client):
    payload = {
        "user_id": "test_user_101",
        "company_name": "Google",
        "target_role": "Backend Engineer"
    }
    response = await client.post("/strategy/dream-company-dna", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Google"
    assert "missing_skills" in data
