"""
Submittal Repository
Provides data access operations for Submittal entities.
"""

from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.submittal import Submittal
from app.repositories.base_repository import BaseRepository


class SubmittalRepository(BaseRepository[Submittal]):
    """Repository for Submittal-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(Submittal, db)

    def get_by_project_id(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Submittal]:
        """
        Get all submittals for a specific project.

        Args:
            project_id: The project ID to filter by
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of Submittal objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self,
        status: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Submittal]:
        """
        Get submittals by status, optionally filtered by project.

        Args:
            status: Submittal status to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Submittal objects
        """
        query = self.db.query(self.model).filter(self.model.status == status)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_submitted_by(
        self,
        user_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Submittal]:
        """
        Get submittals submitted by a specific user.

        Args:
            user_id: User ID who submitted the submittal
            status: Optional status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Submittal objects
        """
        query = self.db.query(self.model).filter(self.model.submitted_by == user_id)

        if status:
            query = query.filter(self.model.status == status)

        return query.offset(skip).limit(limit).all()

    def get_by_reviewed_by(
        self,
        user_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Submittal]:
        """
        Get submittals reviewed by a specific user.

        Args:
            user_id: User ID who reviewed the submittal
            status: Optional status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Submittal objects
        """
        query = self.db.query(self.model).filter(self.model.reviewed_by == user_id)

        if status:
            query = query.filter(self.model.status == status)

        return query.offset(skip).limit(limit).all()

    def search_submittals(
        self,
        search_term: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Submittal]:
        """
        Search submittals by title or description.

        Args:
            search_term: Term to search for in title or description
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching Submittal objects
        """
        search_pattern = f"%{search_term}%"
        query = self.db.query(self.model).filter(
            or_(
                self.model.title.ilike(search_pattern),
                self.model.description.ilike(search_pattern),
            )
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_pending_review(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Submittal]:
        """
        Get submittals pending review (submitted but not reviewed).

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Submittal objects pending review
        """
        query = self.db.query(self.model).filter(self.model.status == "submitted")

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_approved_submittals(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Submittal]:
        """
        Get approved submittals.

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of approved Submittal objects
        """
        query = self.db.query(self.model).filter(self.model.status == "approved")

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_rejected_submittals(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Submittal]:
        """
        Get rejected submittals.

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of rejected Submittal objects
        """
        query = self.db.query(self.model).filter(self.model.status == "rejected")

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Submittal]:
        """
        Get submittals within a date range.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Submittal objects within the date range
        """
        query = self.db.query(self.model)

        if start_date:
            query = query.filter(self.model.submitted_date >= start_date)

        if end_date:
            query = query.filter(self.model.submitted_date <= end_date)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()
