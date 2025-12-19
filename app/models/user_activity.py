from sqlalchemy import Column, DateTime, Index, String
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import BaseModel


class UserActivity(BaseModel):
    """User activity tracking model for managing read/unread items"""

    __tablename__ = "user_activity"

    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)

    # Section visit timestamps
    last_rfis_visit = Column(DateTime(timezone=True), nullable=True)
    last_submittals_visit = Column(DateTime(timezone=True), nullable=True)
    last_change_orders_visit = Column(DateTime(timezone=True), nullable=True)
    last_tasks_visit = Column(DateTime(timezone=True), nullable=True)
    last_documents_visit = Column(DateTime(timezone=True), nullable=True)

    # Individual item reads stored as JSONB
    # Format: {"rfi_123": "2024-01-15T10:30:00Z", "task_456": "2024-01-15T11:00:00Z"}
    read_items = Column(JSONB, nullable=True, default={}, server_default="{}")

    __table_args__ = (Index("ix_user_activity_user_project", "user_id", "project_id"),)

    def __repr__(self):
        return f"<UserActivity(id={self.id}, user_id={self.user_id}, project_id={self.project_id})>"
