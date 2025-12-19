"""
User Pydantic Schemas
Schemas for User entity validation and serialization.
"""

from typing import Optional

from pydantic import EmailStr, Field, field_validator

from app.constants.enums import UserRole
from app.schemas.base import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class UserCreateSchema(BaseCreateSchema):
    """Schema for creating a new user."""

    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=200, description="User full name")
    password: str = Field(
        ..., min_length=8, description="User password (will be hashed)"
    )
    photo: Optional[str] = Field(None, description="URL to user photo")
    role: UserRole = Field(UserRole.USER, description="User role")
    active: bool = Field(True, description="Whether user account is active")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """Validate name is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password meets minimum requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserUpdateSchema(BaseUpdateSchema):
    """Schema for updating an existing user (all fields optional)."""

    email: Optional[EmailStr] = Field(None, description="User email address")
    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="User full name"
    )
    password: Optional[str] = Field(
        None, min_length=8, description="User password (will be hashed)"
    )
    photo: Optional[str] = Field(None, description="URL to user photo")
    role: Optional[UserRole] = Field(None, description="User role")
    active: Optional[bool] = Field(None, description="Whether user account is active")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate name is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Name cannot be empty")
        return v.strip() if v else v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: Optional[str]) -> Optional[str]:
        """Validate password meets minimum requirements if provided."""
        if v is not None and len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserResponseSchema(BaseResponseSchema):
    """Schema for user API responses (excludes password_hash)."""

    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    photo: Optional[str] = Field(None, description="URL to user photo")
    role: str = Field(..., description="User role")
    active: bool = Field(..., description="Whether user account is active")


class UserListResponseSchema(BaseResponseSchema):
    """Simplified schema for user lists."""

    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    role: str = Field(..., description="User role")
    active: bool = Field(..., description="Whether user account is active")


class UserLoginSchema(BaseCreateSchema):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserLoginResponseSchema(BaseResponseSchema):
    """Schema for login response."""

    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    role: str = Field(..., description="User role")
    token: str = Field(..., description="JWT authentication token")
    token_type: str = Field("bearer", description="Token type")


class PasswordChangeSchema(BaseCreateSchema):
    """Schema for changing user password."""

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate new password meets minimum requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
