"""
Activity Log Routes
API endpoints for activity log retrieval and management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository
from app.schemas import ActivityLogListResponseSchema, ActivityLogResponseSchema
from app.utils.dependencies import get_current_user, require_admin
from app.utils.exceptions import ensure_exists, raise_bad_request

router = APIRouter(prefix="/activity-logs", tags=["activity-logs"])


@router.get("", response_model=list[ActivityLogListResponseSchema])
async def list_activity_logs(
    project_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of activity logs with optional filters."""
    activity_repo = ActivityLogRepository(db)

    if entity_id:
        logs = activity_repo.get_by_entity_id(entity_id, skip=skip, limit=limit)
    elif start_date or end_date:
        logs = activity_repo.get_by_date_range(
            start_date=start_date,
            end_date=end_date,
            project_id=project_id,
            skip=skip,
            limit=limit,
        )
    elif project_id and user_id:
        logs = activity_repo.get_by_user_id(
            user_id, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id and action:
        logs = activity_repo.get_by_action(
            action, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id and entity_type:
        logs = activity_repo.get_by_entity_type(
            entity_type, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id:
        logs = activity_repo.get_by_project_id(project_id, skip=skip, limit=limit)
    elif user_id:
        logs = activity_repo.get_by_user_id(user_id, skip=skip, limit=limit)
    elif action:
        logs = activity_repo.get_by_action(action, skip=skip, limit=limit)
    elif entity_type:
        logs = activity_repo.get_by_entity_type(entity_type, skip=skip, limit=limit)
    else:
        logs = activity_repo.get_all(skip=skip, limit=limit)

    return logs


@router.get("/recent", response_model=list[ActivityLogListResponseSchema])
async def get_recent_activity(
    project_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get recent activity logs."""
    activity_repo = ActivityLogRepository(db)
    logs = activity_repo.get_recent_activity(project_id=project_id, limit=limit)
    return logs


@router.get("/summary/by-user")
async def get_activity_summary_by_user(
    project_id: str = Query(..., description="Project ID is required"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get activity summary grouped by user."""
    activity_repo = ActivityLogRepository(db)
    summary = activity_repo.get_activity_summary_by_user(
        project_id=project_id, start_date=start_date, end_date=end_date
    )
    return summary


@router.get("/summary/by-action")
async def get_activity_summary_by_action(
    project_id: str = Query(..., description="Project ID is required"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get activity summary grouped by action type."""
    activity_repo = ActivityLogRepository(db)
    summary = activity_repo.get_activity_summary_by_action(
        project_id=project_id, start_date=start_date, end_date=end_date
    )
    return summary


@router.get("/{log_id}", response_model=ActivityLogResponseSchema)
async def get_activity_log(
    log_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific activity log by ID."""
    activity_repo = ActivityLogRepository(db)
    log = activity_repo.get_by_id(log_id)
    ensure_exists(log, "Log", log_id)

    return log


@router.delete("/cleanup", status_code=status.HTTP_204_NO_CONTENT)
async def cleanup_old_logs(
    days_to_keep: int = Query(
        90, ge=1, le=365, description="Number of days of logs to keep"
    ),
    project_id: Optional[str] = Query(
        None, description="Optional project ID to limit cleanup"
    ),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Delete old activity logs (admin only).
    Useful for data pruning to manage storage.
    """
    activity_repo = ActivityLogRepository(db)

    if not activity_repo.delete_old_logs(
        days_to_keep=days_to_keep, project_id=project_id
    ):
        raise_bad_request("Failed to delete old logs")
