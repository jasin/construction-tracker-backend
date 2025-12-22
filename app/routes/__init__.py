"""
Routes package
Aggregates all API route modules.
"""

from fastapi import APIRouter

from app.routes import (
    activity_logs,
    change_orders,
    clients,
    documents,
    projects,
    rfis,
    submittals,
    tasks,
    user_activity,
    users,
)

# Create main API router
api_router = APIRouter(prefix="/api")

# Include all route modules
api_router.include_router(users.auth_router)  # Authentication routes (/api/auth/...)
api_router.include_router(users.router)  # User management routes (/api/users/...)
api_router.include_router(clients.router)
api_router.include_router(tasks.router)
api_router.include_router(projects.router)
api_router.include_router(rfis.router)
api_router.include_router(submittals.router)
api_router.include_router(change_orders.router)
api_router.include_router(documents.router)
api_router.include_router(activity_logs.router)
api_router.include_router(user_activity.router)  # User activity tracking

__all__ = ["api_router"]
