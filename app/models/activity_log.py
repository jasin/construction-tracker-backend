from sqlalchemy import JSON, Column, String

from app.models.base import BaseModel


class ActivityLog(BaseModel):
    """Activity log model for tracking user actions and changes"""

    __tablename__ = "activity_log"

    project_id = Column(String, nullable=True, index=True)
    user_id = Column(String, nullable=True, index=True)
    user_name = Column(String, nullable=True)
    action = Column(
        String, nullable=False, index=True
    )  # task_created, project_updated, etc.
    entity_type = Column(String, nullable=True, index=True)  # task, project, rfi, etc.
    entity_id = Column(String, nullable=True, index=True)
    description = Column(String, nullable=True)
    timestamp = Column(String, nullable=False, index=True)  # ISO 8601 timestamp
    additional_data = Column(JSON, nullable=True, default=dict)  # Any extra metadata

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, action={self.action}, entity_type={self.entity_type})>"
