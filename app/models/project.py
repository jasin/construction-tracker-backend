from sqlalchemy import Column, Float, String

from app.models.base import BaseModel


class Project(BaseModel):
    """Project model for construction projects"""

    __tablename__ = "projects"

    name = Column(String, nullable=False)
    job_number = Column(String, nullable=True, index=True)
    client_id = Column(String, nullable=True, index=True)
    phase = Column(
        String, nullable=False, default="pre-construction"
    )  # pre-construction, construction, close-out, complete
    status = Column(
        String, nullable=False, default="active"
    )  # active, on-hold, completed, cancelled
    cost = Column(Float, nullable=True)
    start_date = Column(String, nullable=True)  # ISO 8601 date string
    end_date = Column(String, nullable=True)  # ISO 8601 date string
    project_manager = Column(String, nullable=True)  # User ID
    superintendent = Column(String, nullable=True)  # User ID
    architect = Column(String, nullable=True)

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, phase={self.phase})>"
