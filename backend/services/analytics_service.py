import uuid
import logging
from typing import Dict, Any
from datetime import datetime
from backend.services.firestore_service import firestore_service

logger = logging.getLogger("analytics_service")

class AnalyticsService:
    def log_event(self, event_type: str, user_id: str, payload: Dict[str, Any] = None):
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        event_data = {
            "event_id": event_id,
            "event_type": event_type,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload or {}
        }
        logger.info(f"[ANALYTICS_EVENT] {event_type} for user {user_id}: {payload}")
        try:
            firestore_service.set_document("events", event_id, event_data)
        except Exception as e:
            logger.warning(f"Failed to persist event {event_id} to Firestore: {e}")
        return event_data

analytics_service = AnalyticsService()

