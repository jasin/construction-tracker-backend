import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class BaseModel(Base):
    """Base model with common fields for all entities"""

    __abstract__ = True  # This ensures SQLAlchemy doesn't create a table for this class

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
