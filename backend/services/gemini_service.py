import json
import logging
import re
from typing import Dict, Any, Optional
from backend.config import settings

logger = logging.getLogger("gemini_service")

class GeminiService:
    def __init__(self):
        self.client = None
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("Gemini Client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize google-genai Client: {e}")
        else:
            logger.info("GEMINI_API_KEY not configured. Operating with resilient rule-based/mock AI generator.")

    def generate_json(self, prompt: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends prompt to Gemini API and parses JSON response.
        Falls back to fallback_data on any exception or invalid output.
        """
        if not self.client:
            return fallback_data

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )
            text = response.text if hasattr(response, 'text') else str(response)
            parsed = self._extract_json(text)
            if parsed and isinstance(parsed, dict):
                return parsed
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}. Utilizing fallback data.")

        return fallback_data

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        try:
            # First try direct parse
            return json.loads(text)
        except Exception:
            pass

        # Try extract markdown codeblock ```json ... ```
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        # Try extract first { ... }
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        return None

gemini_service = GeminiService()
