RESUME_ANALYSIS_PROMPT = """
You are the Resume Intelligence Engine for Placement OS.
Analyze the following candidate resume text. Never invent information not supported by the resume.

RESUME TEXT:
{resume_text}

Extract structured insights and generate resume-grounded questions.

Return ONLY a JSON object:
{{
    "extracted_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
    "projects": [
        {{
            "name": "E-Commerce Microservices",
            "description": "Built event-driven backend service for order processing",
            "tech_stack": ["Python", "FastAPI", "RabbitMQ", "PostgreSQL"]
        }}
    ],
    "technologies": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "RabbitMQ"],
    "experience": [],
    "achievements": ["Hackathon Top 3 Winner"],
    "resume_score": 78.0,
    "improvement_suggestions": [
        "Quantify project impact with explicit performance metrics (e.g. reduced latency by 30%).",
        "Add explicit details on database indexing and query optimization."
    ],
    "resume_grounded_questions": [
        "In your E-Commerce Microservices project, how did you handle duplicate messages in RabbitMQ?",
        "Why did you choose PostgreSQL over a document store like MongoDB for order processing?"
    ]
}}
"""

JOB_MATCH_PROMPT = """
You are the Resume-to-Job Matching Engine for Placement OS.
Compare the candidate's resume with the target job description.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{job_description}

Evaluate match percentage, matched skills, missing skills, supporting evidence, and actionable recommendations.

Return ONLY a JSON object:
{{
    "match_score": 75.0,
    "matched_skills": ["Python", "FastAPI", "REST API Design", "Docker"],
    "missing_skills": ["Kubernetes", "gRPC", "CI/CD Pipeline Configuration"],
    "evidence": ["Candidate demonstrated strong FastAPI and Docker usage in past project work."],
    "recommendations": [
        "Build a minikube local deployment project to demonstrate Kubernetes basics.",
        "Add CI/CD GitHub Actions workflow file to your existing GitHub project repository."
    ]
}}
"""
