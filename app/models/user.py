from sqlalchemy import Boolean, Column, String

from app.models.base import BaseModel


class User(BaseModel):
    """User model for authentication and authorization"""

    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)  # Hashed password
    name = Column(String, nullable=False)
    photo = Column(String, nullable=True)  # URL to profile photo
    role = Column(
        String, nullable=False, default="user"
    )  # admin, project-manager, etc.
    active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
