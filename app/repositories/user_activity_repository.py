from datetime import datetime
from typing import Dict, Optional

from sqlalchemy.orm import Session

from app.models.user_activity import UserActivity
from app.repositories.base_repository import BaseRepository


class UserActivityRepository(BaseRepository[UserActivity]):
    """Repository for user activity operations"""

    def __init__(self, db: Session):
        super().__init__(db, UserActivity)

    def get_or_create(
        self, user_id: str, project_id: str, created_by: Optional[str] = None
    ) -> UserActivity:
        """
        Get existing user activity record or create new one.
        Ensures one record per user per project.
        """
        activity = (
            self.db.query(UserActivity)
            .filter(
                UserActivity.user_id == user_id, UserActivity.project_id == project_id
            )
            .first()
        )

        if not activity:
            activity = self.create(
                {
                    "user_id": user_id,
                    "project_id": project_id,
                    "read_items": {},
                },
                created_by=created_by,
            )

        return activity

    def update_section_visit(
        self,
        user_id: str,
        project_id: str,
        section: str,
        timestamp: Optional[datetime] = None,
    ) -> UserActivity:
        """
        Update the last visit timestamp for a specific section.

        Args:
            user_id: User ID
            project_id: Project ID
            section: Section name (rfis, submittals, change_orders, tasks, documents)
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Updated UserActivity record
        """
        activity = self.get_or_create(user_id, project_id, created_by=user_id)

        if timestamp is None:
            timestamp = datetime.utcnow()

        # Map section name to database column
        column_map = {
            "rfis": "last_rfis_visit",
            "submittals": "last_submittals_visit",
            "change_orders": "last_change_orders_visit",
            "tasks": "last_tasks_visit",
            "documents": "last_documents_visit",
        }

        column_name = column_map.get(section)
        if not column_name:
            raise ValueError(f"Invalid section: {section}")

        setattr(activity, column_name, timestamp)
        activity.updated_by = user_id

        self.db.commit()
        self.db.refresh(activity)

        return activity

    def mark_item_read(
        self,
        user_id: str,
        project_id: str,
        entity_type: str,
        entity_id: str,
        timestamp: Optional[datetime] = None,
    ) -> UserActivity:
        """
        Mark a specific item as read.

        Args:
            user_id: User ID
            project_id: Project ID
            entity_type: Entity type (rfi, submittal, change_order, task, document)
            entity_id: Entity ID
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Updated UserActivity record
        """
        activity = self.get_or_create(user_id, project_id, created_by=user_id)

        if timestamp is None:
            timestamp = datetime.utcnow()

        # Ensure read_items is a dict
        if activity.read_items is None:
            activity.read_items = {}

        # Update read_items JSONB
        item_key = f"{entity_type}_{entity_id}"
        activity.read_items[item_key] = timestamp.isoformat()

        # Mark the JSONB column as modified for SQLAlchemy to detect change
        from sqlalchemy.orm.attributes import flag_modified

        flag_modified(activity, "read_items")

        activity.updated_by = user_id

        self.db.commit()
        self.db.refresh(activity)

        return activity

    def get_by_user_and_project(
        self, user_id: str, project_id: str
    ) -> Optional[UserActivity]:
        """Get user activity record for specific user and project"""
        return (
            self.db.query(UserActivity)
            .filter(
                UserActivity.user_id == user_id, UserActivity.project_id == project_id
            )
            .first()
        )

    def clear_read_items(self, user_id: str, project_id: str) -> UserActivity:
        """Clear all read items for a user in a project"""
        activity = self.get_or_create(user_id, project_id, created_by=user_id)
        activity.read_items = {}

        from sqlalchemy.orm.attributes import flag_modified

        flag_modified(activity, "read_items")

        activity.updated_by = user_id

        self.db.commit()
        self.db.refresh(activity)

        return activity

    def clear_section_visits(self, user_id: str, project_id: str) -> UserActivity:
        """Clear all section visit timestamps for a user in a project"""
        activity = self.get_or_create(user_id, project_id, created_by=user_id)

        activity.last_rfis_visit = None
        activity.last_submittals_visit = None
        activity.last_change_orders_visit = None
        activity.last_tasks_visit = None
        activity.last_documents_visit = None
        activity.updated_by = user_id

        self.db.commit()
        self.db.refresh(activity)

        return activity
