"""
Task Routes
API endpoints for task management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository, TaskRepository
from app.schemas import (
    TaskCreateSchema,
    TaskListResponseSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
)
from app.utils.dependencies import get_current_user
from app.utils.exceptions import (
    ensure_exists,
    ensure_operation_success,
    raise_bad_request,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskListResponseSchema])
async def list_tasks(
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned user"),
    category: Optional[str] = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of tasks with optional filters."""
    task_repo = TaskRepository(db)

    # Apply filters based on query parameters
    if project_id and status:
        tasks = task_repo.get_by_status(
            status, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id and priority:
        tasks = task_repo.get_by_priority(
            priority, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id and category:
        tasks = task_repo.get_by_category(
            category, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id:
        tasks = task_repo.get_by_project_id(project_id, skip=skip, limit=limit)
    elif assigned_to and status:
        tasks = task_repo.get_by_assigned_to(
            assigned_to, status=status, skip=skip, limit=limit
        )
    elif assigned_to:
        tasks = task_repo.get_by_assigned_to(assigned_to, skip=skip, limit=limit)
    elif status:
        tasks = task_repo.get_by_status(status, skip=skip, limit=limit)
    elif priority:
        tasks = task_repo.get_by_priority(priority, skip=skip, limit=limit)
    else:
        tasks = task_repo.get_all(skip=skip, limit=limit)

    return tasks


@router.get("/overdue", response_model=list[TaskListResponseSchema])
async def list_overdue_tasks(
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get overdue tasks."""
    task_repo = TaskRepository(db)
    tasks = task_repo.get_overdue_tasks(project_id=project_id, skip=skip, limit=limit)
    return tasks


@router.get("/due-soon", response_model=list[TaskListResponseSchema])
async def list_tasks_due_soon(
    days: int = Query(7, ge=1, le=90, description="Number of days ahead to look"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get tasks due within specified number of days."""
    task_repo = TaskRepository(db)
    tasks = task_repo.get_tasks_due_soon(
        days=days, project_id=project_id, skip=skip, limit=limit
    )
    return tasks


@router.get("/search", response_model=list[TaskListResponseSchema])
async def search_tasks(
    q: str = Query(..., min_length=1, description="Search term"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search tasks by title or description."""
    task_repo = TaskRepository(db)
    tasks = task_repo.search_tasks(q, project_id=project_id, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific task by ID."""
    task_repo = TaskRepository(db)
    task = ensure_exists(task_repo.get_by_id(task_id), "Task", task_id)

    return task


@router.post("", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task."""
    task_repo = TaskRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Create task
    task = task_repo.create(task_data.model_dump(), created_by=current_user.id)

    # Log activity
    activity_repo.log_activity(
        project_id=str(task.project_id),
        user_id=current_user.id,
        user_name=current_user.name,
        action="task_created",
        entity_type="task",
        entity_id=task.id,
        description=f"Created task: {task.title}",
        additional_data={"priority": task.priority, "status": task.status},
    )

    return task


@router.patch("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: str,
    task_data: TaskUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing task."""
    task_repo = TaskRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if task exists
    ensure_exists(task_repo.get_by_id(task_id), "Task", task_id)

    # Update task
    task = ensure_operation_success(
        task_repo.update(
            task_id,
            task_data.model_dump(exclude_unset=True),
            updated_by=current_user.id,
        ),
        "update",
        "Task",
    )

    # Log activity
    activity_repo.log_activity(
        project_id=str(task.project_id),
        user_id=current_user.id,
        user_name=current_user.name,
        action="task_updated",
        entity_type="task",
        entity_id=task.id,
        description=f"Updated task: {task.title}",
        additional_data=task_data.model_dump(exclude_unset=True),
    )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task."""
    task_repo = TaskRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if task exists
    task = ensure_exists(task_repo.get_by_id(task_id), "Task", task_id)

    # Log activity before deletion
    activity_repo.log_activity(
        project_id=str(task.project_id),
        user_id=current_user.id,
        user_name=current_user.name,
        action="task_deleted",
        entity_type="task",
        entity_id=task.id,
        description=f"Deleted task: {task.title}",
        additional_data={"priority": task.priority, "status": task.status},
    )

    # Delete task
    if not task_repo.delete(task_id):
        raise_bad_request("Failed to delete task")
