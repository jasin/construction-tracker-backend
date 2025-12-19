"""
User Activity Pydantic Schemas
Schemas for UserActivity entity validation and serialization.
"""

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field, field_validator


class SectionVisitUpdate(BaseModel):
    """Schema for updating a section visit timestamp."""

    section: str = Field(
        ...,
        description="Section name (rfis, submittals, change_orders, tasks, documents)",
    )

    @field_validator("section")
    @classmethod
    def validate_section(cls, v: str) -> str:
        """Validate section name."""
        valid_sections = ["rfis", "submittals", "change_orders", "tasks", "documents"]
        if v not in valid_sections:
            raise ValueError(f"Section must be one of: {', '.join(valid_sections)}")
        return v


class MarkItemRead(BaseModel):
    """Schema for marking an item as read."""

    entity_type: str = Field(
        ..., description="Entity type (rfi, submittal, change_order, task, document)"
    )
    entity_id: str = Field(..., description="Entity ID")

    @field_validator("entity_type")
    @classmethod
    def validate_entity_type(cls, v: str) -> str:
        """Validate entity type."""
        valid_types = ["rfi", "submittal", "change_order", "task", "document"]
        if v not in valid_types:
            raise ValueError(f"Entity type must be one of: {', '.join(valid_types)}")
        return v


class UserActivityResponse(BaseModel):
    """Schema for user activity response."""

    id: str = Field(..., description="Activity record ID")
    user_id: str = Field(..., description="User ID")
    project_id: str = Field(..., description="Project ID")
    last_rfis_visit: Optional[datetime] = Field(
        None, description="Last RFIs section visit"
    )
    last_submittals_visit: Optional[datetime] = Field(
        None, description="Last submittals section visit"
    )
    last_change_orders_visit: Optional[datetime] = Field(
        None, description="Last change orders section visit"
    )
    last_tasks_visit: Optional[datetime] = Field(
        None, description="Last tasks section visit"
    )
    last_documents_visit: Optional[datetime] = Field(
        None, description="Last documents section visit"
    )
    read_items: Dict[str, str] = Field(
        default_factory=dict, description="Read items mapping"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
