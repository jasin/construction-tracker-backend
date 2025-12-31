"""
Document Pydantic Schemas
Schemas for Document entity validation and serialization.
"""

from typing import Optional

from pydantic import Field, field_validator

from app.constants.enums import DocumentCategory
from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class DocumentCreateSchema(BaseCreateSchema):
    """Schema for creating a new document."""

    name: str = Field(..., min_length=1, max_length=200, description="Document name")
    type: str = Field(
        ..., max_length=50, description="Document file type (e.g., 'pdf', 'docx')"
    )
    category: DocumentCategory = Field(..., description="Document category")
    url: str = Field(..., description="Document URL (Google Drive or other storage)")
    project_id: str = Field(..., description="Project ID this document belongs to")
    linked_entity_id: Optional[str] = Field(
        None, description="ID of linked entity (task, RFI, etc.)"
    )
    uploaded_by: Optional[str] = Field(
        None, description="User ID who uploaded the document"
    )
    uploaded_date: Optional[str] = Field(None, description="Upload date (ISO format)")
    size: Optional[int] = Field(None, ge=0, description="File size in bytes")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """Validate name is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class DocumentUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing document (all fields optional)."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Document name"
    )
    type: Optional[str] = Field(None, max_length=50, description="Document file type")
    category: Optional[DocumentCategory] = Field(None, description="Document category")
    url: Optional[str] = Field(None, description="Document URL")
    project_id: Optional[str] = Field(
        None, description="Project ID this document belongs to"
    )
    linked_entity_id: Optional[str] = Field(None, description="ID of linked entity")
    uploaded_by: Optional[str] = Field(
        None, description="User ID who uploaded the document"
    )
    uploaded_date: Optional[str] = Field(None, description="Upload date (ISO format)")
    size: Optional[int] = Field(None, ge=0, description="File size in bytes")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate name is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Name cannot be empty")
        return v.strip() if v else v


class DocumentResponseSchema(BaseResponseSchema):
    """Schema for document API responses."""

    name: str = Field(..., description="Document name")
    type: str = Field(..., description="Document file type")
    category: DocumentCategory = Field(..., description="Document category")
    url: str = Field(..., description="Document URL")
    project_id: str = Field(..., description="Project ID this document belongs to")
    linked_entity_id: Optional[str] = Field(None, description="ID of linked entity")
    uploaded_by: Optional[str] = Field(
        None, description="User ID who uploaded the document"
    )
    uploaded_date: Optional[str] = Field(None, description="Upload date (ISO format)")
    size: Optional[int] = Field(None, description="File size in bytes")


class DocumentListResponseSchema(BaseResponseSchema):
    """Simplified schema for document lists."""

    name: str = Field(..., description="Document name")
    type: str = Field(..., description="Document file type")
    category: DocumentCategory = Field(..., description="Document category")
    project_id: str = Field(..., description="Project ID this document belongs to")
    uploaded_by: Optional[str] = Field(
        None, description="User ID who uploaded the document"
    )
    project_id: str = Field(..., description="Project ID this document belongs to")
    uploaded_by: Optional[str] = Field(
        None, description="User ID who uploaded the document"
    )
    uploaded_date: Optional[str] = Field(None, description="Upload date (ISO format)")
    size: Optional[int] = Field(None, description="File size in bytes")
