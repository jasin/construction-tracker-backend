from sqlalchemy import Column, Float, String

from app.models.base import BaseModel


class ChangeOrder(BaseModel):
    """Change Order model for tracking project changes"""

    __tablename__ = "change_orders"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        String, nullable=False, default="pending"
    )  # pending, approved, rejected, implemented
    project_id = Column(String, nullable=False, index=True)
    cost = Column(Float, nullable=True)
    requested_by = Column(String, nullable=True)  # User ID
    requested_date = Column(String, nullable=True)  # ISO 8601 date string
    approved_by = Column(String, nullable=True)  # User ID
    approved_date = Column(String, nullable=True)  # ISO 8601 date string

    def __repr__(self):
        return f"<ChangeOrder(id={self.id}, title={self.title}, status={self.status})>"
