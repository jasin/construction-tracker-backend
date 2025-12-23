from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class RFI(BaseModel):
    """RFI (Request for Information) model"""

    __tablename__ = "rfis"

    title: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[str] = mapped_column(
        String, nullable=False, default="medium"
    )  # critical, high, medium, low
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="open"
    )  # open, pending, answered, closed
    project_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    submitted_by: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # User ID
    submitted_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    assigned_to: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )  # User ID
    due_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    response: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # Response text

    def __repr__(self):
        return f"<RFI(id={self.id}, title={self.title}, status={self.status})>"
