"""
Submittal Routes
API endpoints for submittal management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository, SubmittalRepository
from app.schemas import (
    SubmittalCreateSchema,
    SubmittalListResponseSchema,
    SubmittalResponseSchema,
    SubmittalUpdateSchema,
)
from app.utils.dependencies import get_current_user
from app.utils.exceptions import (
    ensure_exists,
    ensure_operation_success,
    raise_bad_request,
)

router = APIRouter(prefix="/submittals", tags=["submittals"])


@router.get("", response_model=list[SubmittalListResponseSchema])
async def list_submittals(
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    submitted_by: Optional[str] = Query(None),
    reviewed_by: Optional[str] = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
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
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
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
    q: str = Query(..., min_length=1, description="Search term"),
    project_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
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
    submittal = ensure_exists(
        submittal_repo.get_by_id(submittal_id), "Submittal", submittal_id
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
        submittal_data.model_dump(), created_by=current_user.id
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

    ensure_exists(submittal_repo.get_by_id(submittal_id), "Submittal", submittal_id)

    submittal = ensure_operation_success(
        submittal_repo.update(
            submittal_id,
            submittal_data.model_dump(exclude_unset=True),
            updated_by=current_user.id,
        ),
        "update",
        "Submittal",
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


@router.delete("/{submittal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_submittal(
    submittal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a submittal."""
    submittal_repo = SubmittalRepository(db)
    activity_repo = ActivityLogRepository(db)

    submittal = ensure_exists(
        submittal_repo.get_by_id(submittal_id), "Submittal", submittal_id
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

    if not submittal_repo.delete(submittal_id):
        raise_bad_request("Failed to delete submittal")
