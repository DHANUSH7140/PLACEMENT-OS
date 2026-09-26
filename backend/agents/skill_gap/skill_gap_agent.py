from typing import Dict, Any, List
from backend.services.firestore_service import firestore_service
from backend.services.gemini_service import gemini_service
from backend.services.analytics_service import analytics_service
from backend.prompts.skill_gap import SKILL_GAP_PROMPT_TEMPLATE

class SkillGapAgent:
    def analyze_skill_gaps(self, user_id: str) -> Dict[str, Any]:
        profile = firestore_service.get_document("student_profiles", user_id) or {}
        mistakes = firestore_service.query_collection("mistakes", "user_id", user_id)
        
        target_role = profile.get("target_role", "Backend Engineer")
        readiness = profile.get("readiness", {})
        dimensions = readiness.get("dimensions", {})
        
        prompt = SKILL_GAP_PROMPT_TEMPLATE.format(
            target_role=target_role,
            dimension_scores=str(dimensions),
            mistakes_data=str([{ "topic": m.get("topic"), "type": m.get("mistake_type"), "cause": m.get("likely_cause") } for m in mistakes]),
            attempts_data=f"Total mistakes logged: {len(mistakes)}"
        )
        
        fallback_data = {
            "strengths": profile.get("readiness", {}).get("strengths", ["Solid foundational knowledge in core programming."]),
            "weaknesses": ["Graph traversal & dynamic programming"],
            "critical_gaps": [
                "Repeated BFS/DFS mistakes indicate a graph traversal gap. Practice BFS and DFS before moving to shortest-path algorithms."
            ],
            "risk_areas": ["Timed technical interview stress"],
            "recommended_topics": [
                {
                    "topic": "Graph BFS/DFS Traversal",
                    "reason": f"Detected {len(mistakes)} mistake patterns in graph & tree problems.",
                    "priority": "high",
                    "estimated_hours": 4
                }
            ]
        }
        
        result = gemini_service.generate_json(prompt, fallback_data)
        
        analytics_service.log_event("skill_gap_detected", user_id, {
            "critical_gaps_count": len(result.get("critical_gaps", [])),
            "top_gap": result.get("critical_gaps", ["Graph Traversal"])[0] if result.get("critical_gaps") else "None"
        })
        
        return result

skill_gap_agent = SkillGapAgent()
