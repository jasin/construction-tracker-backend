"""
Change Order Pydantic Schemas
Schemas for ChangeOrder entity validation and serialization.
"""

from typing import Optional

from pydantic import Field, field_validator

from app.constants.enums import ChangeOrderStatus
from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class ChangeOrderCreateSchema(BaseCreateSchema):
    """Schema for creating a new change order."""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Change order title"
    )
    description: Optional[str] = Field(None, description="Change order description")
    status: ChangeOrderStatus = Field(
        ChangeOrderStatus.PENDING, description="Change order status"
    )
    project_id: str = Field(..., description="Project ID this change order belongs to")
    cost: Optional[float] = Field(None, ge=0, description="Change order cost impact")
    requested_by: Optional[str] = Field(
        None, description="User ID who requested the change order"
    )
    requested_date: Optional[str] = Field(None, description="Request date (ISO format)")
    approved_by: Optional[str] = Field(
        None, description="User ID who approved the change order"
    )
    approved_date: Optional[str] = Field(None, description="Approval date (ISO format)")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class ChangeOrderUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing change order (all fields optional)."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Change order title"
    )
    description: Optional[str] = Field(None, description="Change order description")
    status: Optional[ChangeOrderStatus] = Field(None, description="Change order status")
    project_id: Optional[str] = Field(
        None, description="Project ID this change order belongs to"
    )
    cost: Optional[float] = Field(None, ge=0, description="Change order cost impact")
    requested_by: Optional[str] = Field(
        None, description="User ID who requested the change order"
    )
    requested_date: Optional[str] = Field(None, description="Request date (ISO format)")
    approved_by: Optional[str] = Field(
        None, description="User ID who approved the change order"
    )
    approved_date: Optional[str] = Field(None, description="Approval date (ISO format)")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v


class ChangeOrderResponseSchema(BaseResponseSchema):
    """Schema for change order API responses."""

    title: str = Field(..., description="Change order title")
    description: Optional[str] = Field(None, description="Change order description")
    status: ChangeOrderStatus = Field(..., description="Change order status")
    project_id: str = Field(..., description="Project ID this change order belongs to")
    cost: Optional[float] = Field(None, ge=0, description="Change order cost impact")
    requested_by: Optional[str] = Field(
        None, description="User ID who requested the change order"
    )
    requested_date: Optional[str] = Field(None, description="Request date (ISO format)")
    approved_by: Optional[str] = Field(
        None, description="User ID who approved the change order"
    )
    approved_date: Optional[str] = Field(None, description="Approval date (ISO format)")


class ChangeOrderListResponseSchema(BaseResponseSchema):
    """Simplified schema for change order lists."""

    title: str = Field(..., description="Change order title")
    status: ChangeOrderStatus = Field(..., description="Change order status")
    project_id: str = Field(..., description="Project ID this change order belongs to")
    cost: Optional[float] = Field(None, ge=0, description="Change order cost impact")
    requested_by: Optional[str] = Field(
        None, description="User ID who requested the change order"
    )
    requested_date: Optional[str] = Field(None, description="Request date (ISO format)")
