"""
User Activity Routes
API endpoints for tracking user activity (read/unread items).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories.user_activity_repository import UserActivityRepository
from app.schemas.user_activity import (
    MarkItemRead,
    SectionVisitUpdate,
    UserActivityResponse,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/user-activity", tags=["user-activity"])


@router.get("/{project_id}", response_model=UserActivityResponse)
async def get_user_activity(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get user activity record for a specific project.
    Creates a new record if one doesn't exist.
    """
    user_activity_repo = UserActivityRepository(db)
    activity = user_activity_repo.get_or_create(
        user_id=current_user.id, project_id=project_id, created_by=current_user.id
    )
    return activity


@router.patch("/{project_id}/section-visit", response_model=UserActivityResponse)
async def update_section_visit(
    project_id: str,
    data: SectionVisitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the last visit timestamp for a section.

    This is called when a user navigates to or views a section
    (e.g., RFIs, Submittals, Tasks, etc.)
    """
    user_activity_repo = UserActivityRepository(db)

    activity = user_activity_repo.update_section_visit(
        user_id=current_user.id,
        project_id=project_id,
        section=data.section,
    )
    return activity


@router.patch("/{project_id}/mark-read", response_model=UserActivityResponse)
async def mark_item_as_read(
    project_id: str,
    data: MarkItemRead,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark a specific item as read.

    This is called when a user clicks on or expands an item
    (e.g., opens an RFI detail, expands a task, etc.)
    """
    user_activity_repo = UserActivityRepository(db)

    activity = user_activity_repo.mark_item_read(
        user_id=current_user.id,
        project_id=project_id,
        entity_type=data.entity_type,
        entity_id=data.entity_id,
    )
    return activity


@router.patch("/{project_id}/clear-read-items", response_model=UserActivityResponse)
async def clear_read_items(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Clear all read items for the current user in a project.
    Useful for testing or if user wants to reset their read status.
    """
    user_activity_repo = UserActivityRepository(db)

    activity = user_activity_repo.clear_read_items(
        user_id=current_user.id, project_id=project_id
    )

    return activity


@router.patch("/{project_id}/clear-section-visits", response_model=UserActivityResponse)
async def clear_section_visits(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Clear all section visit timestamps for the current user in a project.
    Useful for testing or if user wants to reset their visit history.
    """
    user_activity_repo = UserActivityRepository(db)
    activity = user_activity_repo.clear_section_visits(
        user_id=current_user.id, project_id=project_id
    )
    return activity
