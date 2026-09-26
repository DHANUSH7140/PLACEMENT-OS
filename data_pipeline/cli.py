"""
Placement OS Data & Question Intelligence CLI.
Provides commands to seed databases, trigger question ingestion,
inspect data models, and verify pipeline health.
"""

import sys
import json
import argparse
from typing import Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .db.firestore_client import FirestoreDatabase
from .seed.seeder import DatabaseSeeder
from .scheduler.ingestion_service import IngestionService
from .intelligence.pipeline import QuestionIntelligencePipeline, IngestionItem
from .models.question import Question


def cmd_seed(args):
    """Seed the database with questions and student data."""
    seeder = DatabaseSeeder()
    summary = seeder.run_seed()
    print("\n[SUCCESS] Seeding Summary:")
    print(json.dumps(summary, indent=2))


def cmd_ingest(args):
    """Run an ingestion cycle from registered sources."""
    print("[INFO] Running Question Ingestion Pipeline...")
    service = IngestionService()
    result = service.run_ingestion_job(batch_limit=args.limit)
    print("\n[SUCCESS] Ingestion Result:")
    print(json.dumps(result, indent=2))


def cmd_test_dedup(args):
    """Test exact and semantic deduplication against a sample problem."""
    print("[INFO] Testing Deduplication Engine...")
    pipeline = QuestionIntelligencePipeline(similarity_threshold=args.threshold)
    questions = []

    # Insert original
    item1 = IngestionItem(
        raw_text="Given weights and values of N items, put these items in a knapsack of capacity W to get maximum total value in knapsack.",
        title="0/1 Knapsack",
        source_name="source_a",
        category="DSA",
        subcategory="Dynamic Programming",
        companies=["Google"],
    )
    res1 = pipeline.process_item(item1, questions)
    print(f"Item 1: {res1['action']} (ID: {res1['question'].id})")

    # Insert exact duplicate
    item2 = IngestionItem(
        raw_text="Given weights and values of N items, put these items in a knapsack of capacity W to get maximum total value in knapsack.",
        title="Knapsack Problem",
        source_name="source_b",
        companies=["Amazon"],
    )
    res2 = pipeline.process_item(item2, questions)
    print(f"Item 2: {res2['action']} (Match: {res2['match_type']}, Companies: {res2['question'].companies}, Observed Freq: {res2['question'].observed_frequency})")

    # Insert semantic duplicate with slight rewording
    item3 = IngestionItem(
        raw_text="Given values and weights of N items, place these items into a knapsack of capacity W to achieve the maximum total value.",
        title="0-1 Knapsack DP",
        source_name="source_c",
        companies=["Microsoft"],
    )
    res3 = pipeline.process_item(item3, questions)
    print(f"Item 3: {res3['action']} (Match: {res3['match_type']}, Sim Score: {res3['similarity_score']:.2f}, Companies: {res3['question'].companies})")


def cmd_status(args):
    """Check Firestore connection and collection health."""
    db = FirestoreDatabase()
    print("📊 Placement OS Data Service Status:")
    print(f"Project ID: {db.project_id}")
    print(f"Database ID: {db.database_id}")
    print(f"Mode: {'OFFLINE (Local in-memory fallback)' if db.is_offline else 'ONLINE (Live Firestore)'}")
    print(f"Supported Collections ({len(db.COLLECTIONS)}):")
    for col in db.COLLECTIONS:
        items = db.list_documents(col, limit=5)
        print(f"  - {col:20} : {len(items)} sample records found")


def main():
    parser = argparse.ArgumentParser(description="Placement OS Data & Question Intelligence CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # seed
    subparsers.add_parser("seed", help="Seed database with rich initial question bank and student data")

    # ingest
    ingest_parser = subparsers.add_parser("ingest", help="Run ingestion pipeline from monitored sources")
    ingest_parser.add_argument("--limit", type=int, default=20, help="Batch limit per source")

    # test-dedup
    dedup_parser = subparsers.add_parser("test-dedup", help="Test exact & semantic deduplication")
    dedup_parser.add_argument("--threshold", type=float, default=0.85, help="Similarity threshold")

    # status
    subparsers.add_parser("status", help="Inspect database status and collections")

    args = parser.parse_args()

    if args.command == "seed":
        cmd_seed(args)
    elif args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "test-dedup":
        cmd_test_dedup(args)
    elif args.command == "status":
        cmd_status(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
