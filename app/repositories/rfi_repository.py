"""
RFI Repository
Provides data access operations for RFI (Request for Information) entities.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.rfi import RFI
from app.repositories.base_repository import BaseRepository


class RFIRepository(BaseRepository[RFI]):
    """Repository for RFI-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(RFI, db)

    def get_by_project_id(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[RFI]:
        """
        Get all RFIs for a specific project.

        Args:
            project_id: The project ID to filter by
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of RFI objects
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
    ) -> List[RFI]:
        """
        Get RFIs by status, optionally filtered by project.

        Args:
            status: RFI status to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of RFI objects
        """
        query = self.db.query(self.model).filter(self.model.status == status)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_priority(
        self,
        priority: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RFI]:
        """
        Get RFIs by priority level.

        Args:
            priority: Priority level to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of RFI objects
        """
        query = self.db.query(self.model).filter(self.model.priority == priority)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_submitted_by(
        self,
        user_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RFI]:
        """
        Get RFIs submitted by a specific user.

        Args:
            user_id: User ID who submitted the RFI
            status: Optional status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of RFI objects
        """
        query = self.db.query(self.model).filter(self.model.submitted_by == user_id)

        if status:
            query = query.filter(self.model.status == status)

        return query.offset(skip).limit(limit).all()

    def get_by_assigned_to(
        self,
        user_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RFI]:
        """
        Get RFIs assigned to a specific user.

        Args:
            user_id: User ID to filter by
            status: Optional status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of RFI objects
        """
        query = self.db.query(self.model).filter(self.model.assigned_to == user_id)

        if status:
            query = query.filter(self.model.status == status)

        return query.offset(skip).limit(limit).all()

    def get_overdue_rfis(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[RFI]:
        """
        Get RFIs that are past their due date and not closed.

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of overdue RFI objects
        """
        today = datetime.now().date().isoformat()

        query = self.db.query(self.model).filter(
            and_(
                self.model.due_date.isnot(None),
                self.model.due_date < today,
                self.model.status != "closed",
            )
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_rfis_due_soon(
        self,
        days: int = 7,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RFI]:
        """
        Get RFIs due within the specified number of days.

        Args:
            days: Number of days ahead to look for due RFIs
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of RFI objects due soon
        """
        from datetime import timedelta

        today = datetime.now().date()
        future_date = (today + timedelta(days=days)).isoformat()
        today_str = today.isoformat()

        query = self.db.query(self.model).filter(
            and_(
                self.model.due_date.isnot(None),
                self.model.due_date >= today_str,
                self.model.due_date <= future_date,
                self.model.status != "closed",
            )
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def search_rfis(
        self,
        search_term: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RFI]:
        """
        Search RFIs by title or description.

        Args:
            search_term: Term to search for in title or description
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching RFI objects
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

    def get_open_rfis(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[RFI]:
        """
        Get all open RFIs (not closed).

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of open RFI objects
        """
        query = self.db.query(self.model).filter(self.model.status != "closed")

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()
