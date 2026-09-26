from typing import Dict, Any
from datetime import datetime
from backend.services.firestore_service import firestore_service
from backend.services.analytics_service import analytics_service
from backend.schemas.models import StudentProfileOnboard, StudentProfileResponse, ReadinessResult, ReadinessDimensions, NextBestAction, PlacementGPSRoute, RouteNode

class ProfileAgent:
    def onboard_student(self, req: StudentProfileOnboard) -> StudentProfileResponse:
        # Default initial readiness scores (customized if known_skills provided)
        base_score = 60.0 if req.known_skills else 50.0
        
        dimensions = ReadinessDimensions(
            aptitude=base_score,
            dsa=base_score,
            cs_fundamentals=base_score + 5.0,
            sql=base_score + 10.0,
            communication=base_score,
            resume=55.0,
            projects=55.0,
            interview=50.0
        )
        
        overall_score = round(
            (dimensions.aptitude + dimensions.dsa + dimensions.cs_fundamentals + 
             dimensions.sql + dimensions.communication + dimensions.resume + 
             dimensions.projects + dimensions.interview) / 8.0, 1
        )
        
        initial_action = NextBestAction(
            action_id="act_init_diagnostic",
            title="Take Initial Placement Diagnostic Assessment",
            type="take_assessment",
            description=f"Evaluate your baseline skills for target role {req.target_role}.",
            target_dimension="dsa",
            estimated_minutes=30,
            priority="high"
        )
        
        readiness = ReadinessResult(
            overall_score=overall_score,
            dimensions=dimensions,
            strengths=req.known_skills if req.known_skills else ["Eager learner"],
            critical_gaps=["Baseline assessment needed to confirm DSA depth"],
            risk_areas=["Mock interview under timed pressure"],
            next_best_action=initial_action
        )
        
        now_str = datetime.utcnow().isoformat()
        
        profile_data = {
            "user_id": req.user_id,
            "name": req.name,
            "email": req.email,
            "target_role": req.target_role,
            "target_company": req.target_company or "Tier 1 Product Company",
            "preparation_weeks": req.preparation_weeks,
            "current_year_or_exp": req.current_year_or_exp,
            "known_skills": req.known_skills,
            "readiness": readiness.model_dump(),
            "created_at": now_str,
            "updated_at": now_str
        }
        
        # Save to Firestore
        firestore_service.set_document("student_profiles", req.user_id, profile_data)
        
        # Initialize default Placement GPS Route
        initial_route = PlacementGPSRoute(
            user_id=req.user_id,
            current_state="Onboarded - Baseline Assessment Pending",
            destination=f"{req.target_role} @ {req.target_company}",
            route=[
                RouteNode(step_id="step_1", title="Diagnostic & Core Aptitude", category="Aptitude", topics=["Quantitative", "Logical Reasoning"], status="in_progress", estimated_hours=5),
                RouteNode(step_id="step_2", title="Data Structures & Algorithms Core", category="DSA", topics=["Arrays", "Strings", "Linked Lists"], status="pending", estimated_hours=15),
                RouteNode(step_id="step_3", title="Advanced Data Structures", category="DSA", topics=["Trees", "Graphs", "Dynamic Programming"], status="locked", estimated_hours=20),
                RouteNode(step_id="step_4", title="Database & SQL Querying", category="SQL", topics=["Joins", "Subqueries", "Indexing"], status="locked", estimated_hours=10),
                RouteNode(step_id="step_5", title="Resume & System Design Projects", category="Resume", topics=["Project Analysis", "Job Match"], status="locked", estimated_hours=10),
                RouteNode(step_id="step_6", title="Mock Interviews & HR Rounds", category="Interview", topics=["Technical Interview", "Behavioral"], status="locked", estimated_hours=10)
            ],
            blocked_by=[],
            next_action=initial_action,
            route_status="on_track",
            last_recalculated_at=now_str
        )
        firestore_service.set_document("learning_plans", req.user_id, initial_route.model_dump())
        
        # Log analytics event
        analytics_service.log_event("onboarding_completed", req.user_id, {
            "target_role": req.target_role,
            "target_company": req.target_company
        })
        
        return StudentProfileResponse(
            user_id=req.user_id,
            name=req.name,
            email=req.email,
            target_role=req.target_role,
            target_company=req.target_company or "Tier 1 Product Company",
            readiness=readiness,
            created_at=now_str,
            updated_at=now_str
        )

profile_agent = ProfileAgent()
