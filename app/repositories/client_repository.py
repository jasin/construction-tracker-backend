"""
Client Repository
Provides data access operations for Client entities.
"""

from typing import List

from sqlalchemy.orm import Session

from app.models.client import Client
from app.repositories.base_repository import BaseRepository


class ClientRepository(BaseRepository[Client]):
    """Repository for Client-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(Client, db)

    def get_by_email(self, email: str) -> Client:
        """Get client by email address."""
        return self.get_one_by_field("email", email)

    def search_by_name(self, name: str) -> List[Client]:
        """Search clients by name (case-insensitive partial match)."""
        return (
            self.db.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()
        )
