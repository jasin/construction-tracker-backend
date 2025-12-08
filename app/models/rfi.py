from sqlalchemy import Column, String

from app.models.base import BaseModel


class RFI(BaseModel):
    """RFI (Request for Information) model"""

    __tablename__ = "rfis"

    title = Column(String, nullable=False)
    priority = Column(
        String, nullable=False, default="medium"
    )  # critical, high, medium, low
    status = Column(
        String, nullable=False, default="open"
    )  # open, pending, answered, closed
    status = Column(String, nullable=False, default="open")  # open, pending, answered, closed
    project_id = Column(String, nullable=False, index=True)
    submitted_by = Column(String, nullable=True)  # User ID
    submitted_date = Column(String, nullable=True)  # ISO 8601 date string
    assigned_to = Column(String, nullable=True, index=True)  # User ID
    due_date = Column(String, nullable=True)  # ISO 8601 date string
    response = Column(String, nullable=True)  # Response text

    def __repr__(self):
        return f"<RFI(id={self.id}, title={self.title}, status={self.status})>"
