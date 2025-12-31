from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Client(BaseModel):
    """Client model for construction clients"""

    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    contact_person: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name})>"
