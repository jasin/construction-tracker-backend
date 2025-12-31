from typing import Optional

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class User(BaseModel):
    """User model for authentication and authorization"""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Hashed password
    name: Mapped[str] = mapped_column(String, nullable=False)
    photo: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # URL to profile photo
    role: Mapped[str] = mapped_column(
        String, nullable=False, default="user"
    )  # admin, project-manager, etc.
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
