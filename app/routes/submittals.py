"""
Submittal Routes
API endpoints for submittal management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository, SubmittalRepository
from app.schemas import (
    MessageResponse,
    SubmittalCreateSchema,
    SubmittalListResponseSchema,
    SubmittalResponseSchema,
    SubmittalUpdateSchema,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/submittals", tags=["submittals"])


@router.get("", response_model=list[SubmittalListResponseSchema])
async def list_submittals(
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    submitted_by: Optional[str] = Query(None),
    reviewed_by: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of submittals with optional filters."""
    submittal_repo = SubmittalRepository(db)

    if project_id and status:
        submittals = submittal_repo.get_by_status(
            status, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id:
        submittals = submittal_repo.get_by_project_id(
            project_id, skip=skip, limit=limit
        )
    elif submitted_by and status:
        submittals = submittal_repo.get_by_submitted_by(
            submitted_by, status=status, skip=skip, limit=limit
        )
    elif submitted_by:
        submittals = submittal_repo.get_by_submitted_by(
            submitted_by, skip=skip, limit=limit
        )
    elif reviewed_by:
        submittals = submittal_repo.get_by_reviewed_by(
            reviewed_by, skip=skip, limit=limit
        )
    elif status:
        submittals = submittal_repo.get_by_status(status, skip=skip, limit=limit)
    else:
        submittals = submittal_repo.get_all(skip=skip, limit=limit)

    return submittals


@router.get("/pending-review", response_model=list[SubmittalListResponseSchema])
async def list_pending_review(
    project_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get submittals pending review."""
    submittal_repo = SubmittalRepository(db)
    submittals = submittal_repo.get_pending_review(
        project_id=project_id, skip=skip, limit=limit
    )
    return submittals


@router.get("/search", response_model=list[SubmittalListResponseSchema])
async def search_submittals(
    q: str = Query(..., min_length=1),
    project_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search submittals by title or description."""
    submittal_repo = SubmittalRepository(db)
    submittals = submittal_repo.search_submittals(
        q, project_id=project_id, skip=skip, limit=limit
    )
    return submittals


@router.get("/{submittal_id}", response_model=SubmittalResponseSchema)
async def get_submittal(
    submittal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific submittal by ID."""
    submittal_repo = SubmittalRepository(db)
    submittal = submittal_repo.get_by_id(submittal_id)

    if not submittal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submittal not found with ID: {submittal_id}",
        )

    return submittal


@router.post(
    "", response_model=SubmittalResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_submittal(
    submittal_data: SubmittalCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new submittal."""
    submittal_repo = SubmittalRepository(db)
    activity_repo = ActivityLogRepository(db)

    submittal = submittal_repo.create(
        submittal_data.model_dump(), user_id=current_user.id
    )

    activity_repo.log_activity(
        project_id=submittal.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="submittal_created",
        entity_type="submittal",
        entity_id=submittal.id,
        description=f"Created submittal: {submittal.title}",
        additional_data={"status": submittal.status},
    )

    return submittal


@router.patch("/{submittal_id}", response_model=SubmittalResponseSchema)
async def update_submittal(
    submittal_id: str,
    submittal_data: SubmittalUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing submittal."""
    submittal_repo = SubmittalRepository(db)
    activity_repo = ActivityLogRepository(db)

    existing_submittal = submittal_repo.get_by_id(submittal_id)
    if not existing_submittal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submittal not found with ID: {submittal_id}",
        )

    submittal = submittal_repo.update(
        submittal_id,
        submittal_data.model_dump(exclude_unset=True),
        user_id=current_user.id,
    )

    activity_repo.log_activity(
        project_id=submittal.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="submittal_updated",
        entity_type="submittal",
        entity_id=submittal.id,
        description=f"Updated submittal: {submittal.title}",
        additional_data=submittal_data.model_dump(exclude_unset=True),
    )

    return submittal


@router.delete("/{submittal_id}", response_model=MessageResponse)
async def delete_submittal(
    submittal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a submittal."""
    submittal_repo = SubmittalRepository(db)
    activity_repo = ActivityLogRepository(db)

    submittal = submittal_repo.get_by_id(submittal_id)
    if not submittal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submittal not found with ID: {submittal_id}",
        )

    activity_repo.log_activity(
        project_id=submittal.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="submittal_deleted",
        entity_type="submittal",
        entity_id=submittal.id,
        description=f"Deleted submittal: {submittal.title}",
        additional_data={"status": submittal.status},
    )

    submittal_repo.delete(submittal_id)

    return MessageResponse(message=f"Submittal {submittal_id} deleted successfully")
