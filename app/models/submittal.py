from sqlalchemy import Column, String

from app.models.base import BaseModel


class Submittal(BaseModel):
    """Submittal model for construction submittals"""

    __tablename__ = "submittals"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        String, nullable=False, default="pending"
    )  # pending, reviewed, approved, rejected
    project_id = Column(String, nullable=False, index=True)
    submitted_by = Column(String, nullable=True)  # User ID
    submitted_date = Column(String, nullable=True)  # ISO 8601 date string
    reviewed_by = Column(String, nullable=True)  # User ID
    reviewed_date = Column(String, nullable=True)  # ISO 8601 date string

    def __repr__(self):
        return f"<Submittal(id={self.id}, title={self.title}, status={self.status})>"
