from typing import Optional

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ActivityLog(BaseModel):
    """Activity log model for tracking user actions and changes"""

    __tablename__ = "activity_log"

    project_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    user_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    action: Mapped[str] = mapped_column(
        String, nullable=False, index=True
    )  # task_created, project_updated, etc.
    entity_type: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )  # task, project, rfi, etc.
    entity_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    timestamp: Mapped[str] = mapped_column(
        String, nullable=False, index=True
    )  # ISO 8601 timestamp
    additional_data: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, default=dict
    )  # Any extra metadata

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, action={self.action}, entity_type={self.entity_type})>"
