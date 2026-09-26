"""
Firestore Database Client and Repository Layer.
Handles Firestore SDK connections, batch writes, collection references,
and offline local JSON caching fallback for rapid local testing.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from ..config import GCP_PROJECT_ID, FIRESTORE_DATABASE_ID

logger = logging.getLogger(__name__)


class FirestoreDatabase:
    """Encapsulates Firestore client interactions with resilient local fallback."""

    COLLECTIONS = [
        "users",
        "student_profiles",
        "questions",
        "question_attempts",
        "assessments",
        "interviews",
        "mistakes",
        "learning_plans",
        "documents",
        "events",
    ]

    def __init__(self, project_id: str = GCP_PROJECT_ID, database_id: str = FIRESTORE_DATABASE_ID):
        self.project_id = project_id
        self.database_id = database_id
        self._db = None
        self._is_offline = False
        self._offline_store: Dict[str, Dict[str, Dict[str, Any]]] = {
            col: {} for col in self.COLLECTIONS
        }
        self._init_client()

    _cached_db = None
    _db_checked = False
    _cached_is_offline = False

    def _init_client(self):
        # Fast local detection: if not running in Cloud Run and no credentials file specified, operate offline instantly
        has_credentials = "GOOGLE_APPLICATION_CREDENTIALS" in os.environ or "K_SERVICE" in os.environ
        if not has_credentials:
            self._is_offline = True
        elif not self.__class__._db_checked:
            self.__class__._db_checked = True
            try:
                from google.cloud import firestore
                self.__class__._cached_db = firestore.Client(project=self.project_id, database=self.database_id)
                self.__class__._cached_is_offline = False
                logger.info(f"Initialized Firestore Client for project '{self.project_id}', db '{self.database_id}'")
            except Exception as e:
                self.__class__._cached_is_offline = True
                logger.warning(f"Could not connect to live Firestore ({e}). Operating in resilient local storage mode.")

        if has_credentials:
            self._db = self.__class__._cached_db
            self._is_offline = self.__class__._cached_is_offline

        if self._is_offline:
            # Automatically load snapshot if available
            snapshot_path = Path(__file__).resolve().parent.parent / "seed" / "snapshots" / "firestore_snapshot.json"
            if snapshot_path.exists():
                try:
                    with open(snapshot_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            self._offline_store.update(data)
                except Exception:
                    pass

    @property
    def is_offline(self) -> bool:
        return self._is_offline

    def set_document(self, collection_name: str, document_id: str, data: Dict[str, Any]) -> None:
        """Writes or updates a document in the specified collection."""
        if not self._is_offline and self._db is not None:
            try:
                doc_ref = self._db.collection(collection_name).document(document_id)
                doc_ref.set(data)
                return
            except Exception as e:
                logger.warning(f"Live Firestore write failed: {e}. Writing to local store.")

        # Local in-memory store
        if collection_name not in self._offline_store:
            self._offline_store[collection_name] = {}
        self._offline_store[collection_name][document_id] = data

    def get_document(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """Reads a document by ID."""
        if not self._is_offline and self._db is not None:
            try:
                doc_ref = self._db.collection(collection_name).document(document_id)
                snapshot = doc_ref.get()
                if snapshot.exists:
                    return snapshot.to_dict()
                return None
            except Exception as e:
                logger.warning(f"Live Firestore read failed: {e}. Reading from local store.")

        return self._offline_store.get(collection_name, {}).get(document_id)

    def list_documents(self, collection_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Lists documents from a collection."""
        if not self._is_offline and self._db is not None:
            try:
                docs = self._db.collection(collection_name).limit(limit).stream()
                return [d.to_dict() for d in docs]
            except Exception as e:
                logger.warning(f"Live Firestore query failed: {e}. Reading from local store.")

        return list(self._offline_store.get(collection_name, {}).values())[:limit]

    def batch_write(self, collection_name: str, documents: List[Dict[str, Any]], id_key: str = "id") -> int:
        """Writes multiple documents using batch commits."""
        count = 0
        if not self._is_offline and self._db is not None:
            try:
                batch = self._db.batch()
                for doc in documents:
                    doc_id = doc.get(id_key) or doc.get("uid") or doc.get("student_id")
                    if not doc_id:
                        continue
                    ref = self._db.collection(collection_name).document(doc_id)
                    batch.set(ref, doc)
                    count += 1
                batch.commit()
                return count
            except Exception as e:
                logger.warning(f"Batch write failed: {e}. Using local store.")

        # Local fallback
        for doc in documents:
            doc_id = doc.get(id_key) or doc.get("uid") or doc.get("student_id")
            if doc_id:
                self.set_document(collection_name, doc_id, doc)
                count += 1
        return count

    def export_local_snapshot(self, output_dir: str = "data_pipeline/seed/snapshots") -> str:
        """Saves current memory database to JSON snapshots for testing & demos."""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / "firestore_snapshot.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self._offline_store, f, indent=2)
        return str(file_path)
