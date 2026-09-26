import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.config import settings

logger = logging.getLogger("firestore_service")

# Local in-memory fallback store when Firestore is unauthenticated / dev mode
_IN_MEMORY_DB: Dict[str, Dict[str, Any]] = {
    "student_profiles": {},
    "questions": {},
    "question_attempts": {},
    "assessments": {},
    "interviews": {},
    "mistakes": {},
    "learning_plans": {},
    "documents": {}
}

class FirestoreService:
    def __init__(self):
        self.db = None
        try:
            from google.cloud import firestore
            self.db = firestore.Client(project=settings.GCP_PROJECT_ID)
            logger.info("Firestore client initialized successfully.")
        except Exception as e:
            logger.warning(f"Firestore Client initialization skipped/failed: {e}. Using resilient in-memory fallback.")
            self.db = None

    def get_document(self, collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        if self.db:
            try:
                doc = self.db.collection(collection_name).document(doc_id).get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as e:
                logger.error(f"Error fetching document {collection_name}/{doc_id} from Firestore: {e}")
        
        # Fallback to in-memory store
        return _IN_MEMORY_DB.get(collection_name, {}).get(doc_id)

    def set_document(self, collection_name: str, doc_id: str, data: Dict[str, Any]) -> bool:
        data["updated_at"] = datetime.utcnow().isoformat()
        if "created_at" not in data:
            data["created_at"] = data["updated_at"]

        if self.db:
            try:
                self.db.collection(collection_name).document(doc_id).set(data, merge=True)
            except Exception as e:
                logger.error(f"Error writing document {collection_name}/{doc_id} to Firestore: {e}")

        # Always keep in-memory sync for resilience
        if collection_name not in _IN_MEMORY_DB:
            _IN_MEMORY_DB[collection_name] = {}
        _IN_MEMORY_DB[collection_name][doc_id] = data
        return True

    def query_collection(self, collection_name: str, filter_field: str = None, filter_value: Any = None) -> List[Dict[str, Any]]:
        if self.db and filter_field:
            try:
                docs = self.db.collection(collection_name).where(filter_field, "==", filter_value).stream()
                return [d.to_dict() for d in docs]
            except Exception as e:
                logger.error(f"Error querying collection {collection_name}: {e}")

        # In-memory query fallback
        coll = _IN_MEMORY_DB.get(collection_name, {})
        if not filter_field:
            return list(coll.values())
        return [item for item in coll.values() if item.get(filter_field) == filter_value]

firestore_service = FirestoreService()
