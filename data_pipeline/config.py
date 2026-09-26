"""
Configuration settings for PLACEMENT OS Data Pipeline.
Loads settings from environment variables with safe defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "placement-os-hackathon")
GCP_REGION = os.getenv("GCP_REGION", "us-central1")
FIRESTORE_DATABASE_ID = os.getenv("FIRESTORE_DATABASE_ID", "(default)")
GCS_STORAGE_BUCKET = os.getenv("GCS_STORAGE_BUCKET", "placement-os-documents.appspot.com")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

INGESTION_BATCH_SIZE = int(os.getenv("INGESTION_BATCH_SIZE", "50"))
INGESTION_SIMILARITY_THRESHOLD = float(os.getenv("INGESTION_SIMILARITY_THRESHOLD", "0.88"))
ENABLE_GEMINI_ENRICHMENT = os.getenv("ENABLE_GEMINI_ENRICHMENT", "false").lower() == "true"
SCHEDULER_SECRET_TOKEN = os.getenv("SCHEDULER_SECRET_TOKEN", "placement-os-scheduler-auth-token")

# All 26 Supported Taxonomies
SUPPORTED_TAXONOMIES = [
    "DSA",
    "Programming",
    "SQL",
    "DBMS",
    "OS",
    "Computer Networks",
    "OOP",
    "Aptitude",
    "AI",
    "ML",
    "DL",
    "NLP",
    "Computer Vision",
    "Generative AI",
    "Cloud",
    "DevOps",
    "Data Analytics",
    "Power BI",
    "Excel",
    "Web Development",
    "System Design",
    "HR",
    "Behavioral",
    "Communication",
    "Project",
    "Resume",
]

# Valid Document Types in Cloud Storage
SUPPORTED_DOC_TYPES = [
    "resume",
    "project_report",
    "presentation",  # PPT/PPTX
    "readme",
]
