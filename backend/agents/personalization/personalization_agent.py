from typing import Dict, Any
from backend.services.firestore_service import firestore_service
from backend.services.gemini_service import gemini_service
from backend.prompts.personalization import PERSONALIZATION_PROMPT

class PersonalizationAgent:
    def get_personalization(self, user_id: str) -> Dict[str, Any]:
        profile = firestore_service.get_document("student_profiles", user_id) or {}
        readiness = profile.get("readiness", {})
        dimensions = readiness.get("dimensions", {})
        
        weak_dims = [dim for dim, score in dimensions.items() if score < 65.0]
        
        prompt = PERSONALIZATION_PROMPT.format(
            target_role=profile.get("target_role", "Software Engineer"),
            target_company=profile.get("target_company", "Product Company"),
            readiness_score=readiness.get("overall_score", 60.0),
            weak_dimensions=", ".join(weak_dims) if weak_dims else "None"
        )
        
        fallback_data = {
            "personalized_tips": [
                "Solve 2 medium DSA problems daily focusing on queue & stack operations.",
                "Conduct 1 mock technical interview session weekly to boost verbal communication clarity."
            ],
            "recommended_focus": weak_dims[0].upper() if weak_dims else "DSA & System Design",
            "daily_goal_minutes": 60
        }
        
        return gemini_service.generate_json(prompt, fallback_data)

personalization_agent = PersonalizationAgent()
