from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Project(BaseModel):
    """Project model for construction projects"""

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, nullable=False)
    job_number: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    client_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    phase: Mapped[str] = mapped_column(
        String, nullable=False, default="pre-construction"
    )  # pre-construction, construction, close-out, complete
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="active"
    )  # active, on-hold, completed, cancelled
    cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    end_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    project_manager: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # User ID
    superintendent: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # User ID
    architect: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, phase={self.phase})>"
