"""
Project Repository
Provides data access operations for Project entities.
"""

from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(db, Project)

    def get_by_client_id(
        self, client_id: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Get all projects for a specific client.

        Args:
            client_id: The client ID to filter by
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of Project objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.client_id == client_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_phase(
        self, phase: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Get projects by phase.

        Args:
            phase: Project phase to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.phase == phase)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, status: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Get projects by status.

        Args:
            status: Project status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_manager(
        self, manager_id: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Get projects managed by a specific project manager.

        Args:
            manager_id: Project manager ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.project_manager == manager_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_superintendent(
        self, superintendent_id: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Get projects supervised by a specific superintendent.

        Args:
            superintendent_id: Superintendent ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.superintendent == superintendent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_job_number(self, job_number: str) -> Optional[Project]:
        """
        Get a project by its job number (should be unique).

        Args:
            job_number: Job number to search for

        Returns:
            Project object if found, None otherwise
        """
        return (
            self.db.query(self.model)
            .filter(self.model.job_number == job_number)
            .first()
        )

    def search_projects(
        self, search_term: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Search projects by name or job number.

        Args:
            search_term: Term to search for in name or job number
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching Project objects
        """
        search_pattern = f"%{search_term}%"
        return (
            self.db.query(self.model)
            .filter(
                or_(
                    self.model.name.ilike(search_pattern),
                    self.model.job_number.ilike(search_pattern),
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Get all active projects (status = 'active').

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active Project objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.status == "active")
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_projects_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Project]:
        """
        Get projects within a date range.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project objects within the date range
        """
        query = self.db.query(self.model)

        if start_date:
            query = query.filter(self.model.start_date >= start_date)

        if end_date:
            query = query.filter(self.model.end_date <= end_date)

        return query.offset(skip).limit(limit).all()

    def get_projects_by_cost_range(
        self,
        min_cost: Optional[float] = None,
        max_cost: Optional[float] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Project]:
        """
        Get projects within a cost range.

        Args:
            min_cost: Minimum project cost
            max_cost: Maximum project cost
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project objects within the cost range
        """
        query = self.db.query(self.model)

        if min_cost is not None:
            query = query.filter(self.model.cost >= min_cost)

        if max_cost is not None:
            query = query.filter(self.model.cost <= max_cost)

        return query.offset(skip).limit(limit).all()
