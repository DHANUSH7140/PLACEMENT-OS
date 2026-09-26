"""
Document Metadata Model for Firestore.
Stores Cloud Storage references, file attributes, extraction status, and parsed metadata.
Large binary files (PDFs, PPTs, markdown, docs) reside in GCS, while Firestore holds this model.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(..., description="doc_...")
    student_id: str = Field(..., description="UID of student who owns this document")
    document_type: str = Field(..., description="resume, project_report, presentation, readme")
    file_name: str = Field(..., description="Original filename uploaded, e.g. resume_john_doe.pdf")
    mime_type: str = Field(..., description="e.g. application/pdf, text/markdown, application/vnd.ms-powerpoint")
    file_size_bytes: int = Field(..., description="File size in bytes")
    
    # Cloud Storage reference pointers
    gcs_bucket: str = Field(...)
    gcs_blob_path: str = Field(..., description="e.g. users/{uid}/resumes/{timestamp}_{filename}")
    gcs_public_url: Optional[str] = Field(default=None, description="Public CDN or authenticated URL if configured")
    
    # Content & Extraction metadata (populated after Member 2 / Gemini extracts text)
    extracted_text_preview: Optional[str] = Field(default=None, description="First ~500 chars snippet")
    extracted_skills: List[str] = Field(default_factory=list, description="Skills extracted from document")
    extracted_projects: List[str] = Field(default_factory=list, description="Project titles extracted")
    parsing_status: str = Field(default="UPLOADED", description="UPLOADED, PROCESSING, PARSED, ERROR")
    parsing_error: Optional[str] = Field(default=None)
    
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_firestore_dict(self) -> Dict[str, Any]:
        return self.model_dump()
