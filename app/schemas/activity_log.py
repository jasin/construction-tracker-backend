"""
Activity Log Pydantic Schemas
Schemas for ActivityLog entity validation and serialization.
"""

from typing import Any, Optional

from pydantic import Field, field_validator

from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class ActivityLogCreateSchema(BaseCreateSchema):
    """Schema for creating a new activity log entry."""

    project_id: str = Field(..., description="Project ID this activity belongs to")
    user_id: str = Field(..., description="User ID who performed the action")
    user_name: str = Field(..., description="User name for display")
    action: str = Field(
        ...,
        max_length=100,
        description="Action type (e.g., 'task_created', 'rfi_updated')",
    )
    entity_type: str = Field(
        ...,
        max_length=50,
        description="Type of entity (e.g., 'task', 'rfi', 'submittal')",
    )
    entity_id: str = Field(..., description="ID of the entity")
    description: str = Field(
        ..., description="Human-readable description of the action"
    )
    timestamp: Optional[str] = Field(
        None, description="Timestamp (ISO format) - auto-generated if not provided"
    )
    additional_data: Optional[dict[str, Any]] = Field(
        None, description="Additional data as JSON"
    )

    @field_validator("description", "user_name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        """Validate field is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class ActivityLogUpdateSchema(BaseUpdateSchema):
    """Schema for updating an activity log (rare - logs are typically immutable)."""

    project_id: Optional[str] = Field(
        None, description="Project ID this activity belongs to"
    )
    user_id: Optional[str] = Field(None, description="User ID who performed the action")
    user_name: Optional[str] = Field(None, description="User name for display")
    action: Optional[str] = Field(None, max_length=100, description="Action type")
    entity_type: Optional[str] = Field(
        None, max_length=50, description="Type of entity"
    )
    entity_id: Optional[str] = Field(None, description="ID of the entity")
    description: Optional[str] = Field(None, description="Description of the action")
    timestamp: Optional[str] = Field(None, description="Timestamp (ISO format)")
    additional_data: Optional[dict[str, Any]] = Field(
        None, description="Additional data as JSON"
    )


class ActivityLogResponseSchema(BaseResponseSchema):
    """Schema for activity log API responses."""

    project_id: str = Field(..., description="Project ID this activity belongs to")
    user_id: str = Field(..., description="User ID who performed the action")
    user_name: str = Field(..., description="User name for display")
    action: str = Field(..., description="Action type")
    entity_type: str = Field(..., description="Type of entity")
    entity_id: str = Field(..., description="ID of the entity")
    description: str = Field(..., description="Description of the action")
    timestamp: str = Field(..., description="Timestamp (ISO format)")
    additional_data: Optional[dict[str, Any]] = Field(
        None, description="Additional data as JSON"
    )


class ActivityLogListResponseSchema(BaseResponseSchema):
    """Simplified schema for activity log lists (same as full response)."""

    project_id: str = Field(..., description="Project ID this activity belongs to")
    user_id: str = Field(..., description="User ID who performed the action")
    user_name: str = Field(..., description="User name for display")
    action: str = Field(..., description="Action type")
    entity_type: str = Field(..., description="Type of entity")
    entity_id: str = Field(..., description="ID of the entity")
    description: str = Field(..., description="Description of the action")
    timestamp: str = Field(..., description="Timestamp (ISO format)")


class ActivitySummarySchema(BaseCreateSchema):
    """Schema for activity summary by user."""

    user_id: str = Field(..., description="User ID")
    name: str = Field(..., description="User name")
    count: int = Field(..., description="Number of activities")


class ActionSummarySchema(BaseCreateSchema):
    """Schema for activity summary by action type."""

    action: str = Field(..., description="Action type")
    count: int = Field(..., description="Number of occurrences")
