from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Submittal(BaseModel):
    """Submittal model for construction submittals"""

    __tablename__ = "submittals"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="pending"
    )  # pending, reviewed, approved, rejected
    project_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    submitted_by: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # User ID
    submitted_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    reviewed_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # User ID
    reviewed_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string

    def __repr__(self):
        return f"<Submittal(id={self.id}, title={self.title}, status={self.status})>"
