"""
Project Pydantic Schemas
Schemas for Project entity validation and serialization.
"""

from typing import Optional

from pydantic import Field, field_validator

from app.constants.enums import ProjectPhase
from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class ProjectCreateSchema(BaseCreateSchema):
    """Schema for creating a new project."""

    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    job_number: str = Field(
        ..., min_length=1, max_length=50, description="Unique job number"
    )
    client_id: Optional[str] = Field(None, description="Client ID")
    phase: ProjectPhase = Field(
        ProjectPhase.PRE_CONSTRUCTION, description="Project phase"
    )
    status: str = Field("active", max_length=50, description="Project status")
    cost: Optional[float] = Field(None, ge=0, description="Project cost")
    start_date: Optional[str] = Field(
        None, description="Project start date (ISO format)"
    )
    end_date: Optional[str] = Field(None, description="Project end date (ISO format)")
    project_manager: Optional[str] = Field(None, description="Project manager user ID")
    superintendent: Optional[str] = Field(None, description="Superintendent user ID")
    architect: Optional[str] = Field(
        None, max_length=200, description="Architect name or firm"
    )

    @field_validator("name", "job_number")
    @classmethod
    def not_empty(cls, v: str) -> str:
        """Validate field is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class ProjectUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing project (all fields optional)."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Project name"
    )
    job_number: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Unique job number"
    )
    client_id: Optional[str] = Field(None, description="Client ID")
    phase: Optional[ProjectPhase] = Field(None, description="Project phase")
    status: Optional[str] = Field(None, max_length=50, description="Project status")
    cost: Optional[float] = Field(None, ge=0, description="Project cost")
    start_date: Optional[str] = Field(
        None, description="Project start date (ISO format)"
    )
    end_date: Optional[str] = Field(None, description="Project end date (ISO format)")
    project_manager: Optional[str] = Field(None, description="Project manager user ID")
    superintendent: Optional[str] = Field(None, description="Superintendent user ID")
    architect: Optional[str] = Field(
        None, max_length=200, description="Architect name or firm"
    )

    @field_validator("name", "job_number")
    @classmethod
    def not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate field is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be empty")
        return v.strip() if v else v


class ProjectResponseSchema(BaseResponseSchema):
    """Schema for project API responses."""

    name: str = Field(..., description="Project name")
    job_number: str = Field(..., description="Unique job number")
    client_id: Optional[str] = Field(None, description="Client ID")
    phase: str = Field(..., description="Project phase")
    status: str = Field(..., description="Project status")
    cost: Optional[float] = Field(None, description="Project cost")
    start_date: Optional[str] = Field(
        None, description="Project start date (ISO format)"
    )
    end_date: Optional[str] = Field(None, description="Project end date (ISO format)")
    project_manager: Optional[str] = Field(None, description="Project manager user ID")
    superintendent: Optional[str] = Field(None, description="Superintendent user ID")
    architect: Optional[str] = Field(None, description="Architect name or firm")


class ProjectListResponseSchema(BaseResponseSchema):
    """Simplified schema for project lists."""

    name: str = Field(..., description="Project name")
    job_number: str = Field(..., description="Unique job number")
    phase: str = Field(..., description="Project phase")
    status: str = Field(..., description="Project status")
    start_date: Optional[str] = Field(
        None, description="Project start date (ISO format)"
    )
    end_date: Optional[str] = Field(None, description="Project end date (ISO format)")
    project_manager: Optional[str] = Field(None, description="Project manager user ID")
