"""
Task Pydantic Schemas
Schemas for Task entity validation and serialization.
"""

from typing import List, Optional

from pydantic import Field, field_validator

from app.constants.enums import TaskPriority, TaskStatus
from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class TaskCreateSchema(BaseCreateSchema):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: TaskPriority = Field(
        TaskPriority.MEDIUM, description="Task priority level"
    )
    status: TaskStatus = Field(TaskStatus.TODO, description="Task status")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    project_id: str = Field(..., description="Project ID this task belongs to")
    assigned_to: Optional[str] = Field(None, description="User ID task is assigned to")
    assigned_to_name: Optional[str] = Field(
        None, description="Display name of assigned user"
    )
    category: Optional[str] = Field(None, max_length=100, description="Task category")
    estimated_hours: Optional[int] = Field(
        None, ge=0, description="Estimated hours to complete"
    )
    dependencies: Optional[List[str]] = Field(
        default_factory=list, description="List of task IDs this task depends on"
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("dependencies")
    @classmethod
    def dependencies_must_be_list(cls, v):
        """Ensure dependencies is a list."""
        if v is None:
            return []
        if not isinstance(v, list):
            raise ValueError("Dependencies must be a list")
        return v


class TaskUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing task (all fields optional)."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Task title"
    )
    description: Optional[str] = Field(None, description="Task description")
    priority: Optional[TaskPriority] = Field(None, description="Task priority level")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    project_id: Optional[str] = Field(
        None, description="Project ID this task belongs to"
    )
    assigned_to: Optional[str] = Field(None, description="User ID task is assigned to")
    assigned_to_name: Optional[str] = Field(
        None, description="Display name of assigned user"
    )
    category: Optional[str] = Field(None, max_length=100, description="Task category")
    estimated_hours: Optional[int] = Field(
        None, ge=0, description="Estimated hours to complete"
    )
    dependencies: Optional[List[str]] = Field(
        None, description="List of task IDs this task depends on"
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v


class TaskResponseSchema(BaseResponseSchema):
    """Schema for task API responses."""

    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: str = Field(..., description="Task priority level")
    status: str = Field(..., description="Task status")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    project_id: str = Field(..., description="Project ID this task belongs to")
    assigned_to: Optional[str] = Field(None, description="User ID task is assigned to")
    assigned_to_name: Optional[str] = Field(
        None, description="Display name of assigned user"
    )
    category: Optional[str] = Field(None, description="Task category")
    estimated_hours: Optional[int] = Field(
        None, description="Estimated hours to complete"
    )
    dependencies: Optional[List[str]] = Field(
        None, description="List of task IDs this task depends on"
    )


class TaskListResponseSchema(BaseResponseSchema):
    """Simplified schema for task lists (fewer fields for performance)."""

    title: str = Field(..., description="Task title")
    priority: str = Field(..., description="Task priority level")
    status: str = Field(..., description="Task status")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    project_id: str = Field(..., description="Project ID this task belongs to")
    assigned_to: Optional[str] = Field(None, description="User ID task is assigned to")
    assigned_to_name: Optional[str] = Field(
        None, description="Display name of assigned user"
    )
    category: Optional[str] = Field(None, description="Task category")
