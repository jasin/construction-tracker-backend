"""
RFI Pydantic Schemas
Schemas for RFI (Request for Information) entity validation and serialization.
"""

from typing import Optional

from pydantic import Field, field_validator

from app.constants.enums import RFIPriority, RFIStatus
from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class RFICreateSchema(BaseCreateSchema):
    """Schema for creating a new RFI."""

    title: str = Field(..., min_length=1, max_length=200, description="RFI title")
    description: Optional[str] = Field(None, description="RFI description")
    priority: RFIPriority = Field(RFIPriority.MEDIUM, description="RFI priority level")
    status: RFIStatus = Field(RFIStatus.OPEN, description="RFI status")
    project_id: str = Field(..., description="Project ID this RFI belongs to")
    submitted_by: str = Field(..., description="User ID who submitted the RFI")
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
    assigned_to: Optional[str] = Field(None, description="User ID RFI is assigned to")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    response: Optional[str] = Field(None, description="Response to the RFI")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class RFIUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing RFI (all fields optional)."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="RFI title"
    )
    description: Optional[str] = Field(None, description="RFI description")
    priority: Optional[RFIPriority] = Field(None, description="RFI priority level")
    status: Optional[RFIStatus] = Field(None, description="RFI status")
    project_id: Optional[str] = Field(
        None, description="Project ID this RFI belongs to"
    )
    submitted_by: Optional[str] = Field(
        None, description="User ID who submitted the RFI"
    )
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
    assigned_to: Optional[str] = Field(None, description="User ID RFI is assigned to")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    response: Optional[str] = Field(None, description="Response to the RFI")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v


class RFIResponseSchema(BaseResponseSchema):
    """Schema for RFI API responses."""

    title: str = Field(..., description="RFI title")
    description: Optional[str] = Field(None, description="RFI description")
    priority: str = Field(..., description="RFI priority level")
    status: str = Field(..., description="RFI status")
    project_id: str = Field(..., description="Project ID this RFI belongs to")
    submitted_by: str = Field(..., description="User ID who submitted the RFI")
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
    assigned_to: Optional[str] = Field(None, description="User ID RFI is assigned to")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    response: Optional[str] = Field(None, description="Response to the RFI")


class RFIListResponseSchema(BaseResponseSchema):
    """Simplified schema for RFI lists."""

    title: str = Field(..., description="RFI title")
    priority: str = Field(..., description="RFI priority level")
    status: str = Field(..., description="RFI status")
    project_id: str = Field(..., description="Project ID this RFI belongs to")
    submitted_by: str = Field(..., description="User ID who submitted the RFI")
    submitted_date: Optional[str] = Field(
        None, description="Submission date (ISO format)"
    )
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
