"""
Cloud Scheduler & Continuous Ingestion Service.
Supports:
Cloud Scheduler HTTP target -> /api/v1/ingest/trigger -> question processing -> Firestore.
Includes security token verification, batch rate limiting, and execution logging.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from ..config import SCHEDULER_SECRET_TOKEN, INGESTION_BATCH_SIZE
from ..sources.discovery import SourceDiscoveryService
from ..intelligence.pipeline import QuestionIntelligencePipeline
from ..db.firestore_client import FirestoreDatabase
from ..models.question import Question

logger = logging.getLogger(__name__)


class IngestionService:
    """Orchestrates controlled periodic question ingestion."""

    def __init__(self, db: Optional[FirestoreDatabase] = None):
        self.db = db or FirestoreDatabase()
        self.discovery = SourceDiscoveryService()
        self.pipeline = QuestionIntelligencePipeline()

    def verify_auth_token(self, provided_token: Optional[str]) -> bool:
        """Verifies Cloud Scheduler shared secret token."""
        if not SCHEDULER_SECRET_TOKEN:
            return True
        return provided_token == SCHEDULER_SECRET_TOKEN

    def run_ingestion_job(self, source_names: Optional[List[str]] = None, batch_limit: int = INGESTION_BATCH_SIZE) -> Dict[str, Any]:
        """
        Executes an ingestion batch run:
        1. Reads existing questions from Firestore to populate deduplication index
        2. Discovers items from permitted sources
        3. Runs normalization, deduplication, tagging, difficulty, and enrichment
        4. Writes updates to Firestore
        """
        start_time = time.time()
        logger.info(f"Starting scheduled ingestion run at {datetime.now(timezone.utc).isoformat()}")

        # Load existing questions for deduplication
        raw_existing = self.db.list_documents("questions", limit=500)
        existing_questions = []
        for raw in raw_existing:
            try:
                existing_questions.append(Question(**raw))
            except Exception as e:
                logger.debug(f"Skipping malformed question record during load: {e}")

        # Discover & fetch new candidate items
        new_items = self.discovery.discover_and_fetch(source_names=source_names, limit_per_source=batch_limit)

        if not new_items:
            duration = round(time.time() - start_time, 2)
            return {
                "status": "SUCCESS",
                "message": "No new items discovered across monitored sources.",
                "total_processed": 0,
                "inserted": 0,
                "merged": 0,
                "duration_seconds": duration,
            }

        # Process through Question Intelligence Pipeline
        results = self.pipeline.process_batch(new_items, existing_questions)

        # Batch commit to Firestore
        questions_to_commit = [q.to_firestore_dict() for q in existing_questions]
        committed_count = self.db.batch_write("questions", questions_to_commit, id_key="id")

        duration = round(time.time() - start_time, 2)
        summary = {
            "status": "SUCCESS",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "items_discovered": len(new_items),
            "inserted": results["inserted"],
            "merged": results["merged"],
            "exact_duplicates": results["exact_duplicates"],
            "semantic_duplicates": results["semantic_duplicates"],
            "total_questions_in_store": len(existing_questions),
            "firestore_committed_count": committed_count,
            "duration_seconds": duration,
        }

        logger.info(f"Scheduled ingestion completed: {summary}")
        return summary
