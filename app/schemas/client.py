"""
Client Pydantic Schemas
Schemas for Client entity validation and serialization.
"""

from typing import Optional

from pydantic import EmailStr, Field, field_validator

from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class ClientCreateSchema(BaseCreateSchema):
    """Schema for creating a new client."""

    name: str = Field(..., min_length=1, max_length=200, description="Client name")
    email: Optional[EmailStr] = Field(None, description="Client email address")
    phone: Optional[str] = Field(None, max_length=50, description="Client phone number")
    address: Optional[str] = Field(None, max_length=500, description="Client address")
    contact_person: Optional[str] = Field(
        None, max_length=200, description="Primary contact person name"
    )

    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        """Validate field is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class ClientUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing client (all fields optional)."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Client name"
    )
    email: Optional[EmailStr] = Field(None, description="Client email address")
    phone: Optional[str] = Field(None, max_length=50, description="Client phone number")
    address: Optional[str] = Field(None, max_length=500, description="Client address")
    contact_person: Optional[str] = Field(
        None, max_length=200, description="Primary contact person name"
    )


class ClientResponseSchema(BaseResponseSchema):
    """Schema for client response data."""

    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
