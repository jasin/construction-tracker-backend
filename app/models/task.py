from typing import Optional

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Task(BaseModel):
    """Task model for project tasks"""

    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    priority: Mapped[str] = mapped_column(
        String, nullable=False, default="medium"
    )  # critical, high, medium, low
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="todo"
    )  # todo, in-progress, review, complete, on-hold
    due_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    project_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    assigned_to: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )  # User ID
    assigned_to_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    estimated_hours: Mapped[Optional[int]] = mapped_column(nullable=True)
    dependencies: Mapped[Optional[list]] = mapped_column(
        JSON, nullable=True, default=list
    )  # Array of task IDs

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
