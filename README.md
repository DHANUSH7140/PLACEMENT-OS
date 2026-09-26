# PLACEMENT OS — Data & Question Intelligence Architecture

Welcome to **PLACEMENT OS**, the intelligent placement readiness and career acceleration platform.  
This module is owned by **Member 3 (Data Architecture & Question Intelligence)** and delivers the complete Firestore data layer, Question Intelligence Pipeline, Cloud Storage integration, and Scheduler automation.

---

## 🏗️ 4-Member Team Architecture

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│       Member 1: Frontend        │       │        Member 2: Backend        │
│    Lovable UI + Firebase Auth   │ ◄───► │       FastAPI + Gemini AI       │
└────────────────┬────────────────┘       └────────────────┬────────────────┘
                 │                                         │
                 ▼                                         ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                  Member 3: Data & Intelligence (This Module)              │
│  - 10 Firestore Collections & Security Rules                              │
│  - Question Intelligence Pipeline (Normalization, Dedup, Classification)  │
│  - Cloud Storage (Resumes, Reports, PPTs, READMEs)                        │
│  - Cloud Scheduler Trigger & Seed Question Bank                           │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     │
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│               Member 4: Analytics & Cloud Infrastructure                  │
│       Cloud Run Deployment + BigQuery Streaming + Looker Studio           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Question Intelligence Pipeline Flow

```
   Source Discovery (Permitted Curated Sources / JSON Feeds)
              │
              ▼
          Extraction (Text, Metadata, Provenance)
              │
              ▼
        Normalization (Unicode standard, Boilerplate strip, SHA-256 hash)
              │
              ▼
      Exact Deduplication (Hash match -> Merge metadata into canonical)
              │
              ▼
    Semantic Deduplication (Token Dice & N-gram overlap -> Merge metadata)
              │
              ▼
   Classification (26 Canonical Placement Taxonomies & Subcategories)
              │
              ▼
       Entity Tagging (Companies & Roles extracted & normalized)
              │
              ▼
    Difficulty & Student Relevance Estimation (Easy, Medium, Hard)
              │
              ▼
   Gemini Enrichment (Structured explanation, hints, test cases, solution)
              │
              ▼
     Firestore Commit ('questions' collection with composite indexes)
              │
              ▼
      Available to Student (Instant real-time sync on frontend)
```

---

## 📂 Firestore Collections (10 Core Schemas)

1. `questions` — Master question repository across all 26 taxonomies.
2. `users` — Authentication identities and roles (student, mentor, admin).
3. `student_profiles` — Academic info, readiness score, target companies/roles.
4. `question_attempts` — Student code/answer submissions and evaluation scores.
5. `assessments` — Diagnostic and company-specific mock tests.
6. `interviews` — AI mock interview transcripts and rubric scores.
7. `mistakes` — Personalized mistake tracker with spaced repetition revision dates.
8. `learning_plans` — Dynamic 30/60-day milestone placement sprints.
9. `documents` — Metadata & GCS storage pointers for Resumes, PPTs, Reports, READMEs.
10. `events` — Activity and telemetry stream for student engagement.

---

## 📁 Repository Structure

```
PLACEMENT-OS/
├── firestore.rules               # Production Firestore Security Rules
├── firestore.indexes.json        # Composite indexes for querying & sorting
├── storage.rules                 # Cloud Storage rules for resumes, reports, PPTs
├── firebase.json                 # Firebase configuration
├── .gitignore                    # Comprehensive secrets & credentials protection
├── .env.example                  # Environment variable template
├── requirements.txt              # Core Python dependencies
│
├── data_pipeline/                # Member 3 Core Package
│   ├── config.py                 # Configuration & taxonomy constants
│   ├── cli.py                    # Unified CLI for seeding, ingestion & diagnostics
│   ├── db/
│   │   └── firestore_client.py   # Resilient Firestore client with offline fallback
│   ├── models/                   # Pydantic v2 schemas for all 10 collections
│   │   ├── question.py
│   │   ├── student.py
│   │   ├── assessment.py
│   │   └── document.py
│   ├── intelligence/             # Question Intelligence Pipeline
│   │   ├── normalizer.py         # Text & hash normalizer
│   │   ├── deduplicator.py       # Exact hash & token semantic deduplication
│   │   ├── classifier.py         # 26-domain taxonomy classifier
│   │   ├── tagger.py             # Company & role tagger
│   │   ├── difficulty.py         # Cognitive difficulty & relevance estimator
│   │   ├── gemini_enricher.py    # Gemini educational enrichment & test cases
│   │   └── pipeline.py           # End-to-end pipeline orchestrator
│   ├── sources/                  # Controlled sources (curated feed, JSON feeds)
│   ├── storage/                  # Cloud Storage manager & signed URLs
│   ├── scheduler/                # Continuous ingestion & Cloud Scheduler integration
│   └── seed/                     # Realistic seed questions and student data
│
├── contracts/                    # Cross-member integration contracts
│   ├── FIRESTORE_SCHEMA.md       # Canonical schema reference
│   ├── MEMBER1_FRONTEND.md       # Lovable frontend queries & upload flows
│   ├── MEMBER2_BACKEND.md        # FastAPI imports & mistake tracking
│   └── MEMBER4_ANALYTICS.md      # BigQuery stream & Looker Studio views
│
└── tests/                        # Full unit test suite (13 passing tests)
```

---

## 🚀 Quickstart & CLI Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed Database (Demo-Ready)
Populates the realistic question bank across all categories and creates sample student data:
```bash
python -m data_pipeline.cli seed
```

### 3. Run Ingestion Pipeline
Polls monitored sources and processes questions through deduplication and enrichment:
```bash
python -m data_pipeline.cli ingest --limit 20
```

### 4. Test Deduplication
Verifies exact hash matching and semantic paraphrase merging:
```bash
python -m data_pipeline.cli test-dedup
```

### 5. Check Service & Collection Status
```bash
python -m data_pipeline.cli status
```

### 6. Run Test Suite
```bash
pytest tests/
```

---

## 🔒 Security Best Practices
- **Private Data Isolation:** In `firestore.rules`, students can only read and write their own records (`student_id == request.auth.uid`).
- **Binary File Storage:** Binary files (PDFs, DOCX, PPTX) are strictly kept in Cloud Storage with metadata references in Firestore.
- **Secrets Management:** Credentials (`.env`, service account JSONs, API keys) are strictly ignored in `.gitignore`.
