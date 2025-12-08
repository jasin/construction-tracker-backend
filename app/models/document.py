from sqlalchemy import Column, Integer, String

from app.models.base import BaseModel


class Document(BaseModel):
    """Document model for storing document metadata (files stored in Google Drive)"""

    __tablename__ = "documents"

    name = Column(String, nullable=False)
    type = Column(String, nullable=True)  # File extension or MIME type
    category = Column(
        String, nullable=True
    )  # drawing, specification, contract, photo, report, other
    url = Column(String, nullable=False)  # Google Drive link or external URL
    project_id = Column(String, nullable=False, index=True)
    linked_entity_id = Column(
        String, nullable=True, index=True
    )  # ID of related task, RFI, etc.
    uploaded_by = Column(String, nullable=True, index=True)  # User ID
    uploaded_date = Column(String, nullable=True)  # ISO 8601 date string
    size = Column(Integer, nullable=True)  # File size in bytes

    def __repr__(self):
        return f"<Document(id={self.id}, name={self.name}, category={self.category})>"
