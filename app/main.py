from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import api_router

# Note: Database tables should be created via Alembic migrations, not on startup
# This allows the app to start even without a database connection

# Initialize FastAPI app
app = FastAPI(
    title="Construction Tracker API",
    version="1.0.0",
    description="Backend API for Construction Tracker application",
    debug=settings.debug,
)

print("FastAPI app initialized, starting server")

# CORS middleware (allow Vue/iOS/Electron to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/debug")
async def debug():
    """Temporary debug endpoint"""
    return {
        "message": "Debug endpoint working",
        "cors_origins": settings.cors_origins_list,
    }


# Temporarily comment out api_router to test basic app
# app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Construction Tracker API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Run with: uvicorn app.main:app --reload
