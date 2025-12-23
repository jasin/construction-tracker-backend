from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Document(BaseModel):
    """Document model for storing document metadata (files stored in Google Drive)"""

    __tablename__ = "documents"

    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # File extension or MIME type
    category: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # drawing, specification, contract, photo, report, other
    url: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Google Drive link or external URL
    project_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    linked_entity_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )  # ID of related task, RFI, etc.
    uploaded_by: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )  # User ID
    uploaded_date: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # ISO 8601 date string
    size: Mapped[Optional[int]] = mapped_column(nullable=True)  # File size in bytes

    def __repr__(self):
        return f"<Document(id={self.id}, name={self.name}, category={self.category})>"
