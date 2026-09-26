from typing import Dict, Any, Optional
from datetime import datetime
from backend.services.firestore_service import firestore_service
from backend.services.gemini_service import gemini_service
from backend.services.analytics_service import analytics_service
from backend.schemas.models import (
    StrategyNextResponse, NextBestAction, PlacementGPSRoute, RouteNode,
    DreamCompanyDNARequest, DreamCompanyDNAResponse
)
from backend.prompts.strategy import STRATEGY_NEXT_ACTION_PROMPT, DREAM_COMPANY_DNA_PROMPT
from backend.prompts.route import ROUTE_RECALCULATION_PROMPT

class StrategyAgent:
    def get_next_action(self, user_id: str) -> StrategyNextResponse:
        profile = firestore_service.get_document("student_profiles", user_id) or {}
        mistakes = firestore_service.query_collection("mistakes", "user_id", user_id)
        
        target_role = profile.get("target_role", "Backend Engineer")
        readiness = profile.get("readiness", {})
        dimensions = readiness.get("dimensions", {})
        
        prompt = STRATEGY_NEXT_ACTION_PROMPT.format(
            target_role=target_role,
            readiness_scores=str(dimensions),
            mistake_count=len(mistakes),
            recent_activity="Recent assessment and question attempts completed."
        )
        
        fallback_data = {
            "next_best_action": {
                "action_id": "act_dsa_trees_practice",
                "title": "Practice Binary Tree Traversals (BFS/DFS)",
                "type": "practice_topic",
                "description": "Your DSA dimension is currently 61.0%. Solve 3 targeted tree traversal problems.",
                "target_dimension": "dsa",
                "estimated_minutes": 40,
                "priority": "high"
            },
            "rationale": "DSA performance exhibits recurring gaps in tree and graph traversal algorithms.",
            "focus_areas": ["BFS Level Order Traversal", "Binary Search Trees", "Recursion Stack"]
        }
        
        res = gemini_service.generate_json(prompt, fallback_data)
        next_act = NextBestAction(**res.get("next_best_action", fallback_data["next_best_action"]))
        
        return StrategyNextResponse(
            user_id=user_id,
            next_best_action=next_act,
            rationale=res.get("rationale", fallback_data["rationale"]),
            focus_areas=res.get("focus_areas", fallback_data["focus_areas"])
        )

    def get_placement_route(self, user_id: str, force_recalculate: bool = False) -> PlacementGPSRoute:
        plan_doc = firestore_service.get_document("learning_plans", user_id)
        profile = firestore_service.get_document("student_profiles", user_id) or {}
        mistakes = firestore_service.query_collection("mistakes", "user_id", user_id)
        
        target_role = profile.get("target_role", "Backend Engineer")
        target_company = profile.get("target_company", "Tier 1 Product Company")
        
        # Determine if recalculation is needed
        readiness = profile.get("readiness", {})
        dsa_score = readiness.get("dimensions", {}).get("dsa", 60.0)
        
        needs_recalc = force_recalculate or (dsa_score < 65.0) or len(mistakes) > 2
        
        if plan_doc and not needs_recalc:
            return PlacementGPSRoute(**plan_doc)
            
        # Perform AI Route Recalculation
        current_route_steps = plan_doc.get("route", []) if plan_doc else []
        evidence = f"DSA Score: {dsa_score}%, Mistakes Logged: {len(mistakes)}. Repeated tree/graph traversal errors."
        
        prompt = ROUTE_RECALCULATION_PROMPT.format(
            target_role=target_role,
            target_company=target_company,
            current_route_steps=str(current_route_steps),
            performance_evidence=evidence,
            current_state=f"Current readiness: {readiness.get('overall_score', 60.0)}%",
            destination=f"{target_role} @ {target_company}"
        )
        
        now_str = datetime.utcnow().isoformat()
        
        fallback_route = PlacementGPSRoute(
            user_id=user_id,
            current_state=f"Readiness: {readiness.get('overall_score', 60.0)}% - Route Adjusted for Remediation",
            destination=f"{target_role} @ {target_company}",
            route=[
                RouteNode(step_id="step_1", title="Arrays & Hashing Foundations", category="DSA", topics=["Two Pointers", "Sliding Window"], status="completed", estimated_hours=6),
                RouteNode(step_id="step_2", title="Strings & Basic Recursion", category="DSA", topics=["String Parsing", "Recursion Basics"], status="completed", estimated_hours=5),
                RouteNode(step_id="step_3_recalc", title="Tree Fundamentals & Recursion Stack", category="DSA", topics=["Binary Trees", "Node Pointer Traversal"], status="in_progress", estimated_hours=5),
                RouteNode(step_id="step_4_recalc", title="Tree Traversals (DFS/BFS)", category="DSA", topics=["Inorder/Preorder/Postorder", "Queue Level-Order"], status="pending", estimated_hours=6),
                RouteNode(step_id="step_5_recalc", title="BST & Graph Foundations", category="DSA", topics=["BST Validation", "Graph Representations"], status="pending", estimated_hours=8),
                RouteNode(step_id="step_6", title="System Design & Project Review", category="Project", topics=["API Design", "Database Indexing"], status="locked", estimated_hours=10),
                RouteNode(step_id="step_7", title="Final Mock Interview Simulation", category="Interview", topics=["Technical & HR Mock"], status="locked", estimated_hours=6)
            ],
            blocked_by=["Tree Traversal Gap detected in recent assessment"],
            next_action=NextBestAction(
                action_id="act_tree_fundamentals",
                title="Complete Tree Fundamentals Module",
                type="practice_topic",
                description="Master tree node recursion before advancing to complex graph algorithms.",
                target_dimension="dsa",
                estimated_minutes=45,
                priority="high"
            ),
            route_status="recalculated",
            last_recalculated_at=now_str
        )
        
        res = gemini_service.generate_json(prompt, fallback_route.model_dump())
        
        try:
            route_obj = PlacementGPSRoute(**res)
        except Exception:
            route_obj = fallback_route
            
        firestore_service.set_document("learning_plans", user_id, route_obj.model_dump())
        
        analytics_service.log_event("readiness_updated", user_id, {
            "route_recalculated": True,
            "route_status": route_obj.route_status
        })
        
        return route_obj

    def get_dream_company_dna(self, req: DreamCompanyDNARequest) -> DreamCompanyDNAResponse:
        profile = firestore_service.get_document("student_profiles", req.user_id) or {}
        known_skills = profile.get("known_skills", ["Python", "SQL", "FastAPI"])
        
        prompt = DREAM_COMPANY_DNA_PROMPT.format(
            company_name=req.company_name,
            target_role=req.target_role,
            student_skills_summary=f"Known Skills: {', '.join(known_skills)}"
        )
        
        fallback_data = {
            "company_name": req.company_name,
            "target_role": req.target_role,
            "matching_skills": [s for s in known_skills if s in ["Python", "SQL", "FastAPI", "Java", "C++"]],
            "missing_skills": ["Distributed Caching (Redis)", "System Design (Scalability)", "High Throughput Queueing"],
            "weak_areas": ["System Design trade-off explanations", "Advanced Graph Algorithms"],
            "recommended_preparation": [
                f"Solve top 15 high-frequency DSA questions asked in {req.company_name} technical rounds.",
                "Review Low-Level System Design principles and database index optimization."
            ],
            "assumptions_made": [
                "Assumed standard product company tech stack interview structure based on benchmark role data."
            ]
        }
        
        res = gemini_service.generate_json(prompt, fallback_data)
        return DreamCompanyDNAResponse(**res)

strategy_agent = StrategyAgent()
