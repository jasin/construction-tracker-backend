"""
RFI Routes
API endpoints for RFI (Request for Information) management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository, RFIRepository
from app.schemas import (
    MessageResponse,
    RFICreateSchema,
    RFIListResponseSchema,
    RFIResponseSchema,
    RFIUpdateSchema,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/rfis", tags=["rfis"])


@router.get("", response_model=list[RFIListResponseSchema])
async def list_rfis(
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    submitted_by: Optional[str] = Query(None, description="Filter by submitter"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned user"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of RFIs with optional filters."""
    rfi_repo = RFIRepository(db)

    if project_id and status:
        rfis = rfi_repo.get_by_status(
            status, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id and priority:
        rfis = rfi_repo.get_by_priority(
            priority, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id:
        rfis = rfi_repo.get_by_project_id(project_id, skip=skip, limit=limit)
    elif submitted_by and status:
        rfis = rfi_repo.get_by_submitted_by(
            submitted_by, status=status, skip=skip, limit=limit
        )
    elif submitted_by:
        rfis = rfi_repo.get_by_submitted_by(submitted_by, skip=skip, limit=limit)
    elif assigned_to and status:
        rfis = rfi_repo.get_by_assigned_to(
            assigned_to, status=status, skip=skip, limit=limit
        )
    elif assigned_to:
        rfis = rfi_repo.get_by_assigned_to(assigned_to, skip=skip, limit=limit)
    elif status:
        rfis = rfi_repo.get_by_status(status, skip=skip, limit=limit)
    elif priority:
        rfis = rfi_repo.get_by_priority(priority, skip=skip, limit=limit)
    else:
        rfis = rfi_repo.get_all(skip=skip, limit=limit)

    return rfis


@router.get("/open", response_model=list[RFIListResponseSchema])
async def list_open_rfis(
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all open RFIs."""
    rfi_repo = RFIRepository(db)
    rfis = rfi_repo.get_open_rfis(project_id=project_id, skip=skip, limit=limit)
    return rfis


@router.get("/overdue", response_model=list[RFIListResponseSchema])
async def list_overdue_rfis(
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get overdue RFIs."""
    rfi_repo = RFIRepository(db)
    rfis = rfi_repo.get_overdue_rfis(project_id=project_id, skip=skip, limit=limit)
    return rfis


@router.get("/due-soon", response_model=list[RFIListResponseSchema])
async def list_rfis_due_soon(
    days: int = Query(7, ge=1, le=90, description="Number of days ahead to look"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get RFIs due within specified number of days."""
    rfi_repo = RFIRepository(db)
    rfis = rfi_repo.get_rfis_due_soon(
        days=days, project_id=project_id, skip=skip, limit=limit
    )
    return rfis


@router.get("/search", response_model=list[RFIListResponseSchema])
async def search_rfis(
    q: str = Query(..., min_length=1, description="Search term"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search RFIs by title or description."""
    rfi_repo = RFIRepository(db)
    rfis = rfi_repo.search_rfis(q, project_id=project_id, skip=skip, limit=limit)
    return rfis


@router.get("/{rfi_id}", response_model=RFIResponseSchema)
async def get_rfi(
    rfi_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific RFI by ID."""
    rfi_repo = RFIRepository(db)
    rfi = rfi_repo.get_by_id(rfi_id)

    if not rfi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RFI not found with ID: {rfi_id}",
        )

    return rfi


@router.post("", response_model=RFIResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_rfi(
    rfi_data: RFICreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new RFI."""
    rfi_repo = RFIRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Create RFI
    rfi = rfi_repo.create(rfi_data.model_dump(), user_id=current_user.id)

    # Log activity
    activity_repo.log_activity(
        project_id=rfi.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="rfi_created",
        entity_type="rfi",
        entity_id=rfi.id,
        description=f"Created RFI: {rfi.title}",
        additional_data={"priority": rfi.priority, "status": rfi.status},
    )

    return rfi


@router.patch("/{rfi_id}", response_model=RFIResponseSchema)
async def update_rfi(
    rfi_id: str,
    rfi_data: RFIUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing RFI."""
    rfi_repo = RFIRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if RFI exists
    existing_rfi = rfi_repo.get_by_id(rfi_id)
    if not existing_rfi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RFI not found with ID: {rfi_id}",
        )

    # Update RFI
    rfi = rfi_repo.update(
        rfi_id, rfi_data.model_dump(exclude_unset=True), user_id=current_user.id
    )

    # Log activity
    activity_repo.log_activity(
        project_id=rfi.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="rfi_updated",
        entity_type="rfi",
        entity_id=rfi.id,
        description=f"Updated RFI: {rfi.title}",
        additional_data=rfi_data.model_dump(exclude_unset=True),
    )

    return rfi


@router.delete("/{rfi_id}", response_model=MessageResponse)
async def delete_rfi(
    rfi_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an RFI."""
    rfi_repo = RFIRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if RFI exists
    rfi = rfi_repo.get_by_id(rfi_id)
    if not rfi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RFI not found with ID: {rfi_id}",
        )

    # Log activity before deletion
    activity_repo.log_activity(
        project_id=rfi.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="rfi_deleted",
        entity_type="rfi",
        entity_id=rfi.id,
        description=f"Deleted RFI: {rfi.title}",
        additional_data={"priority": rfi.priority, "status": rfi.status},
    )

    # Delete RFI
    rfi_repo.delete(rfi_id)

    return MessageResponse(message=f"RFI {rfi_id} deleted successfully")
