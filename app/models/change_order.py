from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ChangeOrder(BaseModel):
    """Change Order model for tracking project changes"""

    __tablename__ = "change_orders"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="pending"
    )  # pending, approved, rejected, implemented
    project_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    requested_by: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )  # User ID
    requested_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    approved_by: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )  # User ID
    approved_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string

    def __repr__(self):
        return f"<ChangeOrder(id={self.id}, title={self.title}, status={self.status})>"
