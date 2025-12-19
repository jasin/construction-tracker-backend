"""
Task Repository
Provides data access operations for Task entities.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Repository for Task-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_by_project_id(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        Get all tasks for a specific project.

        Args:
            project_id: The project ID to filter by
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of Task objects
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
    ) -> List[Task]:
        """
        Get tasks by status, optionally filtered by project.

        Args:
            status: Task status to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Task objects
        """
        query = self.db.query(self.model).filter(self.model.status == status)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_assigned_to(
        self,
        user_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        """
        Get tasks assigned to a specific user.

        Args:
            user_id: User ID to filter by
            status: Optional status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Task objects
        """
        query = self.db.query(self.model).filter(self.model.assigned_to == user_id)

        if status:
            query = query.filter(self.model.status == status)

        return query.offset(skip).limit(limit).all()

    def get_by_priority(
        self,
        priority: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        """
        Get tasks by priority level.

        Args:
            priority: Priority level to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Task objects
        """
        query = self.db.query(self.model).filter(self.model.priority == priority)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_overdue_tasks(
        self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        Get tasks that are past their due date and not completed.

        Args:
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of overdue Task objects
        """
        today = datetime.now().date().isoformat()

        query = self.db.query(self.model).filter(
            and_(
                self.model.due_date.isnot(None),
                self.model.due_date < today,
                self.model.status != "complete",
            )
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_category(
        self,
        category: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        """
        Get tasks by category.

        Args:
            category: Task category to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Task objects
        """
        query = self.db.query(self.model).filter(self.model.category == category)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def search_tasks(
        self,
        search_term: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            search_term: Term to search for in title or description
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching Task objects
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

    def get_tasks_due_soon(
        self,
        days: int = 7,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        """
        Get tasks due within the specified number of days.

        Args:
            days: Number of days ahead to look for due tasks
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Task objects due soon
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
                self.model.status != "complete",
            )
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()
