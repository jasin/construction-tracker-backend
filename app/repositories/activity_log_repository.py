"""
Activity Log Repository
Provides data access operations for ActivityLog entities.
"""

from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.repositories.base_repository import BaseRepository


class ActivityLogRepository(BaseRepository[ActivityLog]):
    """Repository for ActivityLog-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(ActivityLog, db)

    def get_by_project_id(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[ActivityLog]:
        """
        Get all activity logs for a specific project, ordered by timestamp descending.

        Args:
            project_id: The project ID to filter by
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of ActivityLog objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.project_id == project_id)
            .order_by(desc(self.model.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user_id(
        self,
        user_id: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ActivityLog]:
        """
        Get activity logs by user, optionally filtered by project.

        Args:
            user_id: User ID to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ActivityLog objects ordered by timestamp descending
        """
        query = (
            self.db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(desc(self.model.timestamp))
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_action(
        self,
        action: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ActivityLog]:
        """
        Get activity logs by action type, optionally filtered by project.

        Args:
            action: Action type to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ActivityLog objects ordered by timestamp descending
        """
        query = (
            self.db.query(self.model)
            .filter(self.model.action == action)
            .order_by(desc(self.model.timestamp))
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_entity_type(
        self,
        entity_type: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ActivityLog]:
        """
        Get activity logs by entity type, optionally filtered by project.

        Args:
            entity_type: Entity type to filter by (e.g., 'task', 'rfi', 'submittal')
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ActivityLog objects ordered by timestamp descending
        """
        query = (
            self.db.query(self.model)
            .filter(self.model.entity_type == entity_type)
            .order_by(desc(self.model.timestamp))
        )

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_entity_id(
        self, entity_id: str, skip: int = 0, limit: int = 100
    ) -> List[ActivityLog]:
        """
        Get all activity logs for a specific entity.

        Args:
            entity_id: Entity ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ActivityLog objects ordered by timestamp descending
        """
        return (
            self.db.query(self.model)
            .filter(self.model.entity_id == entity_id)
            .order_by(desc(self.model.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ActivityLog]:
        """
        Get activity logs within a date range.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ActivityLog objects ordered by timestamp descending
        """
        query = self.db.query(self.model).order_by(desc(self.model.timestamp))

        if start_date:
            query = query.filter(self.model.timestamp >= start_date)

        if end_date:
            query = query.filter(self.model.timestamp <= end_date)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_recent_activity(
        self, project_id: Optional[str] = None, limit: int = 50
    ) -> List[ActivityLog]:
        """
        Get the most recent activity logs.

        Args:
            project_id: Optional project ID to filter by
            limit: Maximum number of records to return (default 50)

        Returns:
            List of recent ActivityLog objects ordered by timestamp descending
        """
        query = self.db.query(self.model).order_by(desc(self.model.timestamp))

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.limit(limit).all()

    def log_activity(
        self,
        project_id: Optional[str],
        user_id: str,
        user_name: str,
        action: str,
        entity_type: str,
        entity_id: str,
        description: str,
        additional_data: Optional[dict] = None,
    ) -> Optional[ActivityLog]:
        """
        Create a new activity log entry.

        Args:
            project_id: Project ID (if None, activity logging is silently skipped)
            user_id: User ID performing the action
            user_name: User name for display
            action: Action type (e.g., 'created', 'updated', 'deleted')
            entity_type: Type of entity (e.g., 'task', 'rfi', 'submittal')
            entity_id: ID of the entity
            description: Human-readable description of the action
            additional_data: Optional additional data as JSON

        Returns:
            Created ActivityLog object, or None if project_id was None
        """
        # Guard clause: fail fast if project_id is None
        # This allows callers to pass entity.project_id without None checks
        if project_id is None:
            return None

        from datetime import datetime

        activity_log = ActivityLog(
            project_id=project_id,
            user_id=user_id,
            user_name=user_name,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            timestamp=datetime.now().isoformat(),
            additional_data=additional_data,
        )

        self.db.add(activity_log)
        self.db.commit()
        self.db.refresh(activity_log)

        return activity_log

    def get_activity_summary_by_user(
        self,
        project_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        """
        Get activity summary grouped by user for a project.

        Args:
            project_id: The project ID to analyze
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            Dictionary mapping user IDs to activity counts
        """
        from sqlalchemy import func

        query = self.db.query(
            self.model.user_id, self.model.user_name, func.count(self.model.id)
        ).filter(self.model.project_id == project_id)

        if start_date:
            query = query.filter(self.model.timestamp >= start_date)

        if end_date:
            query = query.filter(self.model.timestamp <= end_date)

        results = query.group_by(self.model.user_id, self.model.user_name).all()

        return {
            user_id: {"name": user_name, "count": count}
            for user_id, user_name, count in results
        }

    def get_activity_summary_by_action(
        self,
        project_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        """
        Get activity summary grouped by action type for a project.

        Args:
            project_id: The project ID to analyze
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            Dictionary mapping actions to counts
        """
        from sqlalchemy import func

        query = self.db.query(self.model.action, func.count(self.model.id)).filter(
            self.model.project_id == project_id
        )

        if start_date:
            query = query.filter(self.model.timestamp >= start_date)

        if end_date:
            query = query.filter(self.model.timestamp <= end_date)

        results = query.group_by(self.model.action).all()

        return {action: count for action, count in results}

    def delete_old_logs(
        self, days_to_keep: int = 90, project_id: Optional[str] = None
    ) -> int:
        """
        Delete activity logs older than specified days.
        Useful for data pruning to manage storage.

        Args:
            days_to_keep: Number of days of logs to keep (default 90)
            project_id: Optional project ID to limit deletion to

        Returns:
            Number of records deleted
        """
        from datetime import datetime, timedelta

        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()

        query = self.db.query(self.model).filter(self.model.timestamp < cutoff_date)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        count = query.count()
        query.delete()
        self.db.commit()

        return count
