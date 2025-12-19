"""
Project Routes
API endpoints for project management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository, ProjectRepository
from app.schemas import (
    MessageResponse,
    ProjectCreateSchema,
    ProjectListResponseSchema,
    ProjectResponseSchema,
    ProjectUpdateSchema,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectListResponseSchema])
async def list_projects(
    client_id: Optional[str] = Query(None, description="Filter by client ID"),
    phase: Optional[str] = Query(None, description="Filter by phase"),
    status: Optional[str] = Query(None, description="Filter by status"),
    manager_id: Optional[str] = Query(None, description="Filter by project manager"),
    superintendent_id: Optional[str] = Query(
        None, description="Filter by superintendent"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of projects with optional filters."""
    project_repo = ProjectRepository(db)

    if client_id:
        projects = project_repo.get_by_client_id(client_id, skip=skip, limit=limit)
    elif phase:
        projects = project_repo.get_by_phase(phase, skip=skip, limit=limit)
    elif status:
        projects = project_repo.get_by_status(status, skip=skip, limit=limit)
    elif manager_id:
        projects = project_repo.get_by_manager(manager_id, skip=skip, limit=limit)
    elif superintendent_id:
        projects = project_repo.get_by_superintendent(
            superintendent_id, skip=skip, limit=limit
        )
    else:
        projects = project_repo.get_all(skip=skip, limit=limit)

    return projects


@router.get("/active", response_model=list[ProjectListResponseSchema])
async def list_active_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all active projects."""
    project_repo = ProjectRepository(db)
    projects = project_repo.get_active_projects(skip=skip, limit=limit)
    return projects


@router.get("/search", response_model=list[ProjectListResponseSchema])
async def search_projects(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search projects by name or job number."""
    project_repo = ProjectRepository(db)
    projects = project_repo.search_projects(q, skip=skip, limit=limit)
    return projects


@router.get("/job-number/{job_number}", response_model=ProjectResponseSchema)
async def get_project_by_job_number(
    job_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a project by its job number."""
    project_repo = ProjectRepository(db)
    project = project_repo.get_by_job_number(job_number)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found with job number: {job_number}",
        )

    return project


@router.get("/{project_id}", response_model=ProjectResponseSchema)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific project by ID."""
    project_repo = ProjectRepository(db)
    project = project_repo.get_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found with ID: {project_id}",
        )

    return project


@router.post(
    "", response_model=ProjectResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project_data: ProjectCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new project."""
    project_repo = ProjectRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if job number already exists
    existing = project_repo.get_by_job_number(project_data.job_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with job number {project_data.job_number} already exists",
        )

    # Create project
    project = project_repo.create(project_data.model_dump(), user_id=current_user.id)

    # Log activity
    activity_repo.log_activity(
        project_id=project.id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="project_created",
        entity_type="project",
        entity_id=project.id,
        description=f"Created project: {project.name}",
        additional_data={"job_number": project.job_number, "phase": project.phase},
    )

    return project


@router.patch("/{project_id}", response_model=ProjectResponseSchema)
async def update_project(
    project_id: str,
    project_data: ProjectUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing project."""
    project_repo = ProjectRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if project exists
    existing_project = project_repo.get_by_id(project_id)
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found with ID: {project_id}",
        )

    # If job number is being updated, check for duplicates
    if (
        project_data.job_number
        and project_data.job_number != existing_project.job_number
    ):
        duplicate = project_repo.get_by_job_number(project_data.job_number)
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project with job number {project_data.job_number} already exists",
            )

    # Update project
    project = project_repo.update(
        project_id, project_data.model_dump(exclude_unset=True), user_id=current_user.id
    )

    # Log activity
    activity_repo.log_activity(
        project_id=project.id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="project_updated",
        entity_type="project",
        entity_id=project.id,
        description=f"Updated project: {project.name}",
        additional_data=project_data.model_dump(exclude_unset=True),
    )

    return project


@router.delete("/{project_id}", response_model=MessageResponse)
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a project."""
    project_repo = ProjectRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if project exists
    project = project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found with ID: {project_id}",
        )

    # Log activity before deletion
    activity_repo.log_activity(
        project_id=project.id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="project_deleted",
        entity_type="project",
        entity_id=project.id,
        description=f"Deleted project: {project.name}",
        additional_data={"job_number": project.job_number},
    )

    # Delete project
    project_repo.delete(project_id)

    return MessageResponse(message=f"Project {project_id} deleted successfully")
