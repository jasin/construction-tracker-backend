from sqlalchemy import JSON, Column, Integer, String

from app.models.base import BaseModel


class Task(BaseModel):
    """Task model for project tasks"""

    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(
        String, nullable=False, default="medium"
    )  # critical, high, medium, low
    status = Column(
        String, nullable=False, default="todo"
    )  # todo, in-progress, review, complete, on-hold
    due_date = Column(String, nullable=True)  # ISO 8601 date string
    project_id = Column(String, nullable=False, index=True)
    assigned_to = Column(String, nullable=True, index=True)  # User ID
    assigned_to_name = Column(String, nullable=True)
    category = Column(String, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    dependencies = Column(JSON, nullable=True, default=list)  # Array of task IDs

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
