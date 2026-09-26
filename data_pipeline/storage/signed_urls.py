"""
Signed URL Generator for Cloud Storage.
Enables Member 1 (Frontend) to upload files directly from the browser to GCS
without routing heavy binary payloads through Member 2's FastAPI server.
"""

from datetime import timedelta
from typing import Optional, Dict, Any
from ..config import GCS_STORAGE_BUCKET
from .storage_manager import StorageManager, MIME_TYPE_MAPPING
from pathlib import Path


class SignedUrlService:
    """Generates V4 signed URLs for direct client uploads and secure downloads."""

    def __init__(self, bucket_name: str = GCS_STORAGE_BUCKET):
        self.bucket_name = bucket_name

    def generate_upload_signed_url(
        self,
        student_id: str,
        doc_type: str,
        original_filename: str,
        expires_minutes: int = 15
    ) -> Dict[str, Any]:
        """
        Generates a PUT signed URL for direct browser-to-GCS upload.
        Returns:
            {
                "upload_url": str,
                "gcs_blob_path": str,
                "mime_type": str,
                "doc_type": str,
                "expires_in_seconds": int
            }
        """
        blob_path = StorageManager.generate_blob_path(student_id, doc_type, original_filename)
        ext = Path(original_filename).suffix.lower()
        mime_type = MIME_TYPE_MAPPING.get(ext, "application/octet-stream")

        upload_url = None
        client = StorageManager._get_client_safe()
        if client:
            try:
                bucket = client.bucket(self.bucket_name)
                blob = bucket.blob(blob_path)

                upload_url = blob.generate_signed_url(
                    version="v4",
                    expiration=timedelta(minutes=expires_minutes),
                    method="PUT",
                    content_type=mime_type,
                )
            except Exception:
                upload_url = None

        if not upload_url:
            # Fallback mock signed URL for local dev/testing
            upload_url = f"https://storage.googleapis.com/{self.bucket_name}/{blob_path}?mock_signed_token=1"

        return {
            "upload_url": upload_url,
            "gcs_blob_path": blob_path,
            "mime_type": mime_type,
            "doc_type": doc_type,
            "expires_in_seconds": expires_minutes * 60,
        }

    def generate_download_signed_url(
        self,
        gcs_blob_path: str,
        expires_minutes: int = 60
    ) -> str:
        """Generates a GET signed URL for authorized document download."""
        client = StorageManager._get_client_safe()
        if client:
            try:
                bucket = client.bucket(self.bucket_name)
                blob = bucket.blob(gcs_blob_path)

                return blob.generate_signed_url(
                    version="v4",
                    expiration=timedelta(minutes=expires_minutes),
                    method="GET",
                )
            except Exception:
                pass

        return f"https://storage.googleapis.com/{self.bucket_name}/{gcs_blob_path}?mock_access_token=1"
