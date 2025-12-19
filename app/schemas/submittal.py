"""
Submittal Pydantic Schemas
Schemas for Submittal entity validation and serialization.
"""

from typing import Optional

from pydantic import Field, field_validator

from app.constants.enums import SubmittalStatus
from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class SubmittalCreateSchema(BaseCreateSchema):
    """Schema for creating a new submittal."""

    title: str = Field(..., min_length=1, max_length=200, description="Submittal title")
    description: Optional[str] = Field(None, description="Submittal description")
    status: SubmittalStatus = Field(
        SubmittalStatus.PENDING, description="Submittal status"
    )
    project_id: str = Field(..., description="Project ID this submittal belongs to")
    submitted_by: Optional[str] = Field(
        None, description="User ID who submitted the submittal"
    )
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
    reviewed_by: Optional[str] = Field(
        None, description="User ID who reviewed the submittal"
    )
    reviewed_date: Optional[str] = Field(None, description="Review date (ISO format)")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class SubmittalUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing submittal (all fields optional)."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Submittal title"
    )
    description: Optional[str] = Field(None, description="Submittal description")
    status: Optional[SubmittalStatus] = Field(None, description="Submittal status")
    project_id: Optional[str] = Field(
        None, description="Project ID this submittal belongs to"
    )
    submitted_by: Optional[str] = Field(
        None, description="User ID who submitted the submittal"
    )
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
    reviewed_by: Optional[str] = Field(
        None, description="User ID who reviewed the submittal"
    )
    reviewed_date: Optional[str] = Field(None, description="Review date (ISO format)")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v


class SubmittalResponseSchema(BaseResponseSchema):
    """Schema for submittal API responses."""

    title: str = Field(..., description="Submittal title")
    description: Optional[str] = Field(None, description="Submittal description")
    status: str = Field(..., description="Submittal status")
    project_id: str = Field(..., description="Project ID this submittal belongs to")
    submitted_by: Optional[str] = Field(
        None, description="User ID who submitted the submittal"
    )
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
    reviewed_by: Optional[str] = Field(
        None, description="User ID who reviewed the submittal"
    )
    reviewed_date: Optional[str] = Field(None, description="Review date (ISO format)")


class SubmittalListResponseSchema(BaseResponseSchema):
    """Simplified schema for submittal lists."""

    title: str = Field(..., description="Submittal title")
    status: str = Field(..., description="Submittal status")
    project_id: str = Field(..., description="Project ID this submittal belongs to")
    submitted_by: Optional[str] = Field(
        None, description="User ID who submitted the submittal"
    )
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
