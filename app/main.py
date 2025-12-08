from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base

# Create database tables (for development - use Alembic in production)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Construction Tracker API",
    version="1.0.0",
    description="Backend API for Construction Tracker application",
    debug=settings.debug
)

# CORS middleware (allow Vue/iOS/Electron to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Include routers when created
# app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
# app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
# app.include_router(websockets.router, prefix="/ws", tags=["websockets"])

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Construction Tracker API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Run with: uvicorn app.main:app --reload
