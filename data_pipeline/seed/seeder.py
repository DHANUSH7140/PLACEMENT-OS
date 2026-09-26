"""
Database Seeder Runner for Placement OS.
Processes the seed questions through the Question Intelligence Pipeline,
attaches full metadata, and commits all 10 collections to Firestore.
Also exports a local JSON snapshot for offline demonstrations and test runs.
"""

import logging
from typing import Dict, Any, List
from .questions_seed_data import SEED_QUESTIONS
from .student_seed_data import (
    SEED_USERS,
    SEED_STUDENT_PROFILES,
    SEED_DOCUMENTS,
    SEED_LEARNING_PLANS,
    SEED_ASSESSMENTS,
    SEED_INTERVIEWS,
    SEED_QUESTION_ATTEMPTS,
    SEED_MISTAKES,
    SEED_EVENTS,
)
from ..intelligence.pipeline import QuestionIntelligencePipeline, IngestionItem
from ..db.firestore_client import FirestoreDatabase
from ..models.question import Question

logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """Orchestrates comprehensive initial seeding."""

    def __init__(self, db: FirestoreDatabase = None):
        self.db = db or FirestoreDatabase()
        self.pipeline = QuestionIntelligencePipeline()

    def run_seed(self) -> Dict[str, Any]:
        """Runs the entire seeding process across all collections."""
        print("[START] Placement OS Database Seeder...")

        # 1. Ingest & Process Seed Questions through Question Intelligence Pipeline
        processed_questions: List[Question] = []
        ingestion_items = [
            IngestionItem(
                raw_text=q["problem_statement"],
                title=q["title"],
                source_name="curated_seed_bank",
                source_url=f"https://placementos.dev/curated/{q['category'].lower()}",
                source_item_id=f"seed_{idx}",
                category=q.get("category"),
                subcategory=q.get("subcategory"),
                topic=q.get("topic"),
                difficulty=q.get("difficulty"),
                companies=q.get("companies"),
                roles=q.get("roles"),
                question_type=q.get("question_type", "Coding"),
                options=q.get("options"),
                correct_answer=q.get("correct_answer"),
                observed_frequency=q.get("observed_frequency", 1),
            )
            for idx, q in enumerate(SEED_QUESTIONS)
        ]

        batch_result = self.pipeline.process_batch(ingestion_items, processed_questions)
        print(f"[SUCCESS] Questions Processed: {batch_result['inserted']} new, {batch_result['merged']} merged duplicates.")

        # Enrich seeded questions with specific solutions / code if present in seed
        for q_model in processed_questions:
            matching_raw = next((r for r in SEED_QUESTIONS if r["title"] == q_model.title), None)
            if matching_raw:
                if "solution_approach" in matching_raw:
                    q_model.solution_approach = matching_raw["solution_approach"]
                if "learning_hints" in matching_raw:
                    q_model.learning_hints = matching_raw["learning_hints"]

        # Commit Questions
        q_dicts = [q.to_firestore_dict() for q in processed_questions]
        q_count = self.db.batch_write("questions", q_dicts, id_key="id")
        print(f"[COMMITTED] {q_count} questions to Firestore 'questions' collection.")

        # 2. Commit Student Profiles & User Data
        u_count = self.db.batch_write("users", SEED_USERS, id_key="uid")
        sp_count = self.db.batch_write("student_profiles", SEED_STUDENT_PROFILES, id_key="student_id")
        doc_count = self.db.batch_write("documents", SEED_DOCUMENTS, id_key="id")
        lp_count = self.db.batch_write("learning_plans", SEED_LEARNING_PLANS, id_key="id")
        asm_count = self.db.batch_write("assessments", SEED_ASSESSMENTS, id_key="id")
        intv_count = self.db.batch_write("interviews", SEED_INTERVIEWS, id_key="id")
        qa_count = self.db.batch_write("question_attempts", SEED_QUESTION_ATTEMPTS, id_key="id")
        m_count = self.db.batch_write("mistakes", SEED_MISTAKES, id_key="id")
        evt_count = self.db.batch_write("events", SEED_EVENTS, id_key="id")

        # 3. Export Snapshot
        snapshot_file = self.db.export_local_snapshot()
        print(f"[EXPORTED] Local Firestore snapshot to: {snapshot_file}")

        summary = {
            "questions": q_count,
            "users": u_count,
            "student_profiles": sp_count,
            "documents": doc_count,
            "learning_plans": lp_count,
            "assessments": asm_count,
            "interviews": intv_count,
            "question_attempts": qa_count,
            "mistakes": m_count,
            "events": evt_count,
            "snapshot_file": snapshot_file,
            "is_offline_mode": self.db.is_offline,
        }
        print("[COMPLETE] Placement OS Seeding Complete!")
        return summary
