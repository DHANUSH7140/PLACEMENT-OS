import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Placement OS Backend API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8080"))
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    GCP_PROJECT_ID: str = os.getenv("GOOGLE_CLOUD_PROJECT", "placement-os-dev")
    FIRESTORE_EMULATOR_HOST: str = os.getenv("FIRESTORE_EMULATOR_HOST", "")
    SCHEDULER_SECRET: str = os.getenv("SCHEDULER_SECRET", "placement_os_secret_token")

settings = Settings()

