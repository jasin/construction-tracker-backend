from sqlalchemy import Column, String

from app.models.base import BaseModel


class Client(BaseModel):
    """Client model for construction clients"""

    __tablename__ = "clients"

    name = Column(String, nullable=False)
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    contact_person = Column(String, nullable=True)

    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name})>"
