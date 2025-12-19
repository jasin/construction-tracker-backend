"""
Change Order Repository
Provides data access operations for ChangeOrder entities.
"""

from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.change_order import ChangeOrder
from app.repositories.base_repository import BaseRepository


class ChangeOrderRepository(BaseRepository[ChangeOrder]):
    """Repository for ChangeOrder-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(ChangeOrder, db)

    def get_by_project_id(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[ChangeOrder]:
        """
        Get all change orders for a specific project.

        Args:
            project_id: The project ID to filter by
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of ChangeOrder objects
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
    ) -> List[ChangeOrder]:
        """
        Get change orders by status, optionally filtered by project.

        Args:
            status: Change order status to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ChangeOrder objects
        """
        query = self.db.query(self.model).filter(self.model.status == status)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_requested_by(
        self,
        user_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ChangeOrder]:
        """
        Get change orders requested by a specific user.

        Args:
            user_id: User ID who requested the change order
            status: Optional status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ChangeOrder objects
        """
        query = self.db.query(self.model).filter(self.model.requested_by == user_id)

        if status:
            query = query.filter(self.model.status == status)

        return query.offset(skip).limit(limit).all()

    def get_by_approved_by(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[ChangeOrder]:
        """
        Get change orders approved by a specific user.

        Args:
            user_id: User ID who approved the change order
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ChangeOrder objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.approved_by == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_change_orders(
        self,
        search_term: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ChangeOrder]:
        """
        Search change orders by title or description.

        Args:
            search_term: Term to search for in title or description
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching ChangeOrder objects
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

    def get_pending_approval(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[ChangeOrder]:
        """
        Get change orders pending approval.

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ChangeOrder objects pending approval
        """
        query = self.db.query(self.model).filter(self.model.status == "pending")

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_approved_change_orders(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[ChangeOrder]:
        """
        Get approved change orders.

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of approved ChangeOrder objects
        """
        query = self.db.query(self.model).filter(self.model.status == "approved")

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_rejected_change_orders(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[ChangeOrder]:
        """
        Get rejected change orders.

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of rejected ChangeOrder objects
        """
        query = self.db.query(self.model).filter(self.model.status == "rejected")

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_cost_range(
        self,
        min_cost: Optional[float] = None,
        max_cost: Optional[float] = None,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ChangeOrder]:
        """
        Get change orders within a cost range.

        Args:
            min_cost: Minimum cost
            max_cost: Maximum cost
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ChangeOrder objects within the cost range
        """
        query = self.db.query(self.model)

        if min_cost is not None:
            query = query.filter(self.model.cost >= min_cost)

        if max_cost is not None:
            query = query.filter(self.model.cost <= max_cost)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_total_cost_by_project(self, project_id: str) -> float:
        """
        Calculate total cost of all change orders for a project.

        Args:
            project_id: The project ID to calculate for

        Returns:
            Total cost of all change orders (0.0 if none)
        """
        from sqlalchemy import func

        result = (
            self.db.query(func.sum(self.model.cost))
            .filter(self.model.project_id == project_id)
            .scalar()
        )

        return result if result is not None else 0.0

    def get_approved_cost_by_project(self, project_id: str) -> float:
        """
        Calculate total cost of approved change orders for a project.

        Args:
            project_id: The project ID to calculate for

        Returns:
            Total cost of approved change orders (0.0 if none)
        """
        from sqlalchemy import func

        result = (
            self.db.query(func.sum(self.model.cost))
            .filter(
                self.model.project_id == project_id, self.model.status == "approved"
            )
            .scalar()
        )

        return result if result is not None else 0.0

    def get_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ChangeOrder]:
        """
        Get change orders within a date range.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ChangeOrder objects within the date range
        """
        query = self.db.query(self.model)

        if start_date:
            query = query.filter(self.model.requested_date >= start_date)

        if end_date:
            query = query.filter(self.model.requested_date <= end_date)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()
