import pytest
import httpx
from backend.main import app

@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.anyio
async def test_complete_student_flow(client):
    user_id = "flow_user_999"
    
    # 1. Onboard Student Profile
    onboard_payload = {
        "user_id": user_id,
        "name": "Sarah Connor",
        "email": "sarah@example.com",
        "target_role": "Backend Engineer",
        "target_company": "Tier 1 Product Company",
        "preparation_weeks": 12,
        "known_skills": ["Python", "SQL"]
    }
    res = await client.post("/profile/onboard", json=onboard_payload)
    assert res.status_code == 200
    profile_data = res.json()
    initial_readiness = profile_data["readiness"]["overall_score"]
    
    # 2. Get Dashboard
    dash_res = await client.get(f"/dashboard?user_id={user_id}")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["user_id"] == user_id
    assert dash_data["placement_route"]["route_status"] in ["on_track", "recalculated"]
    
    # 3. Start Assessment
    start_asm = await client.post("/assessment/start", json={"user_id": user_id, "category": "DSA", "question_count": 2})
    assert start_asm.status_code == 200
    asm_data = start_asm.json()
    asm_id = asm_data["assessment_id"]
    q1_id = asm_data["questions"][0]["question_id"]
    
    # 4. Attempt Question (Wrong Answer to create Mistake)
    att_res = await client.post(f"/questions/{q1_id}/attempt", json={
        "user_id": user_id,
        "question_id": q1_id,
        "submitted_answer": "Wrong Answer Choice",
        "time_taken_seconds": 45
    })
    assert att_res.status_code == 200
    assert att_res.json()["is_correct"] is False
    assert att_res.json()["mistake_logged"] is True
    
    # 5. Check Mistake Memory
    mst_res = await client.get(f"/mistakes?user_id={user_id}")
    assert mst_res.status_code == 200
    mst_data = mst_res.json()
    assert mst_data["total_count"] >= 1
    
    # 6. Submit Assessment with low score to trigger route recalculation
    sub_res = await client.post(f"/assessment/{asm_id}/submit", json={
        "user_id": user_id,
        "answers": [
            {"question_id": q1_id, "submitted_answer": "Wrong Answer Choice", "time_taken_seconds": 45}
        ]
    })
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert sub_data["overall_score"] == 0.0
    assert sub_data["route_recalculated"] is True
    
    # 7. Check Placement Route Recalculation
    route_res = await client.get(f"/placement-route?user_id={user_id}")
    assert route_res.status_code == 200
    route_data = route_res.json()
    assert len(route_data["route"]) > 0
    assert len(route_data["blocked_by"]) >= 1
    
    # 8. Check Strategy Next Best Action
    strat_res = await client.get(f"/strategy/next?user_id={user_id}")
    assert strat_res.status_code == 200
    strat_data = strat_res.json()
    assert "next_best_action" in strat_data
    assert strat_data["next_best_action"]["priority"] == "high"

    # 9. Start AI Interview Session & Submit Candidate Answer
    int_start = await client.post("/interview/start", json={
        "user_id": user_id,
        "interview_type": "technical",
        "target_role": "Backend Engineer",
        "target_company": "Tier 1 Product Company"
    })
    assert int_start.status_code == 200
    int_id = int_start.json()["interview_id"]
    
    int_ans = await client.post(f"/interview/{int_id}/answer", json={
        "user_id": user_id,
        "candidate_answer": "I use queue-based BFS traversal to traverse tree levels sequentially in O(V+E) time."
    })
    assert int_ans.status_code == 200
    ans_data = int_ans.json()
    assert ans_data["evaluation"]["correctness"] >= 70.0
    assert ans_data["next_question"] is not None or ans_data["is_completed"] is True

    # 10. Document Signed Upload URL & Document Registration
    doc_url_res = await client.post("/document/upload-url", json={
        "user_id": user_id,
        "filename": "resume_sarah.pdf",
        "doc_type": "resume"
    })
    assert doc_url_res.status_code == 200
    doc_url_data = doc_url_res.json()
    assert "upload_url" in doc_url_data
    doc_id = doc_url_data["document_id"]
    
    doc_reg_res = await client.post("/document/register", json={
        "user_id": user_id,
        "document_id": doc_id,
        "gcs_path": doc_url_data["gcs_path"],
        "doc_type": "resume",
        "filename": "resume_sarah.pdf",
        "extracted_text": "Sarah Connor - Backend Developer with Python, FastAPI, and SQL experience."
    })
    assert doc_reg_res.status_code == 200
    assert doc_reg_res.json()["status"] == "registered"

    # 11. Scheduler Ingestion Endpoint Authentication & Trigger
    # Unauthenticated attempt (should fail with 401)
    unauth_ingest = await client.post("/api/v1/ingest/trigger")
    assert unauth_ingest.status_code == 401
    
    # Authenticated attempt with scheduler secret
    auth_ingest = await client.post("/api/v1/ingest/trigger", headers={"X-Scheduler-Secret": "placement_os_secret_token"})
    assert auth_ingest.status_code == 200
    assert auth_ingest.json()["status"] == "success"

