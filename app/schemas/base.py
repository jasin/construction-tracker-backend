"""
Base Pydantic Schemas
Provides base schemas with common fields for all entities.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM mode for SQLAlchemy models
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields (for responses)."""

    created_at: datetime = Field(..., description="Timestamp when record was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when record was last updated"
    )


class MetadataSchema(TimestampSchema):
    """Schema with full metadata fields (for responses)."""

    created_by: Optional[str] = Field(
        None, description="User ID who created the record"
    )
    updated_by: Optional[str] = Field(
        None, description="User ID who last updated the record"
    )


class BaseCreateSchema(BaseSchema):
    """Base schema for create operations (no ID or metadata)."""

    pass


class BaseUpdateSchema(BaseSchema):
    """Base schema for update operations (all fields optional)."""

    pass


class BaseResponseSchema(BaseSchema):
    """Base schema for API responses (includes ID and metadata)."""

    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Timestamp when record was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when record was last updated"
    )
    created_by: Optional[str] = Field(
        None, description="User ID who created the record"
    )
    updated_by: Optional[str] = Field(
        None, description="User ID who last updated the record"
    )


class PaginatedResponse(BaseSchema):
    """Generic paginated response wrapper."""

    items: list = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    skip: int = Field(0, description="Number of items skipped")
    limit: int = Field(100, description="Maximum number of items returned")

    @property
    def has_more(self) -> bool:
        """Check if there are more items available."""
        return (self.skip + len(self.items)) < self.total


class MessageResponse(BaseSchema):
    """Simple message response."""

    message: str = Field(..., description="Response message")
    success: bool = Field(True, description="Operation success status")


class ErrorResponse(BaseSchema):
    """Error response."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    success: bool = Field(False, description="Operation success status")
