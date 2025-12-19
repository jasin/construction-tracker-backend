"""
User Repository
Provides data access operations for User entities.
"""

from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by their email address.

        Args:
            email: Email address to search for

        Returns:
            User object if found, None otherwise
        """
        return self.db.query(self.model).filter(self.model.email == email).first()

    def get_by_role(self, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with a specific role.

        Args:
            role: User role to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of User objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.role == role)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active User objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_inactive_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all inactive users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of inactive User objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.active == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_users(
        self, search_term: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """
        Search users by name or email.

        Args:
            search_term: Term to search for in name or email
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching User objects
        """
        search_pattern = f"%{search_term}%"
        return (
            self.db.query(self.model)
            .filter(
                or_(
                    self.model.name.ilike(search_pattern),
                    self.model.email.ilike(search_pattern),
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def email_exists(self, email: str) -> bool:
        """
        Check if an email address is already registered.

        Args:
            email: Email address to check

        Returns:
            True if email exists, False otherwise
        """
        return (
            self.db.query(self.model).filter(self.model.email == email).first()
            is not None
        )

    def get_users_by_roles(
        self, roles: List[str], skip: int = 0, limit: int = 100
    ) -> List[User]:
        """
        Get users with any of the specified roles.

        Args:
            roles: List of roles to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of User objects matching any of the roles
        """
        return (
            self.db.query(self.model)
            .filter(self.model.role.in_(roles))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def deactivate_user(self, user_id: str) -> Optional[User]:
        """
        Deactivate a user account.

        Args:
            user_id: ID of user to deactivate

        Returns:
            Updated User object if found, None otherwise
        """
        user = self.get_by_id(user_id)
        if user:
            user.active = False
            self.db.commit()
            self.db.refresh(user)
        return user

    def activate_user(self, user_id: str) -> Optional[User]:
        """
        Activate a user account.

        Args:
            user_id: ID of user to activate

        Returns:
            Updated User object if found, None otherwise
        """
        user = self.get_by_id(user_id)
        if user:
            user.active = True
            self.db.commit()
            self.db.refresh(user)
        return user

    def update_password_hash(self, user_id: str, password_hash: str) -> Optional[User]:
        """
        Update a user's password hash.

        Args:
            user_id: ID of user to update
            password_hash: New password hash

        Returns:
            Updated User object if found, None otherwise
        """
        user = self.get_by_id(user_id)
        if user:
            user.password_hash = password_hash
            self.db.commit()
            self.db.refresh(user)
        return user
