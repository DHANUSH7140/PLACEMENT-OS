import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger("analytics_service")

# Analytics events:
# login, onboarding_completed, assessment_started, assessment_completed, question_attempted,
# interview_started, interview_completed, resume_analyzed, skill_gap_detected, mission_completed, readiness_updated

class AnalyticsService:
    def log_event(self, event_type: str, user_id: str, payload: Dict[str, Any] = None):
        event_data = {
            "event_type": event_type,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload or {}
        }
        logger.info(f"[ANALYTICS_EVENT] {event_type} for user {user_id}: {payload}")
        # Member 4 can pick up these structured log events or stream them directly to BigQuery
        return event_data

analytics_service = AnalyticsService()
