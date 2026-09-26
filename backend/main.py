import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Placement OS - AI-Powered Placement Readiness Platform API Engine"
)

# Configure CORS middleware for Lovable Frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from Lovable dev server & deployed frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include core API routes
app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Placement OS API Backend",
        "docs_url": "/docs",
        "health_check": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
