from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Base repository with CRUD operations for all models.
    Mirrors the pattern from Firebase repositories in the Vue app.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_by_id(self, id: str) -> Optional[ModelType]:
        """Get single record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def create(
        self, data: Dict[str, Any], created_by: Optional[str] = None
    ) -> ModelType:
        """
        Create new record with metadata.
        Automatically sets created_by and updated_by.
        """
        # Add metadata
        data["created_by"] = created_by
        data["updated_by"] = created_by

        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(
        self, id: str, data: Dict[str, Any], updated_by: Optional[str] = None
    ) -> Optional[ModelType]:
        """
        Update existing record.
        Only updates fields provided in data dict.
        Automatically sets updated_by and updated_at.
        """
        instance = self.get_by_id(id)
        if not instance:
            return None

        # Update fields
        for key, value in data.items():
            if value is not None and hasattr(instance, key):
                setattr(instance, key, value)

        # Update metadata
        if updated_by is not None:
            setattr(instance, "updated_by", updated_by)
        # updated_at is handled by SQLAlchemy's onupdate

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: str) -> bool:
        """
        Delete record by ID.
        Returns True if deleted, False if not found.
        """
        instance = self.get_by_id(id)
        if not instance:
            return False

        self.db.delete(instance)
        self.db.commit()
        return True

    def get_by_field(self, field: str, value: Any) -> List[ModelType]:
        """
        Get records by any field value.
        Example: get_by_field('status', 'active')
        """
        return (
            self.db.query(self.model).filter(getattr(self.model, field) == value).all()
        )

    def get_one_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get single record by field value"""
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, field) == value)
            .first()
        )

    def count(self) -> int:
        """Get total count of records"""
        return self.db.query(self.model).count()

    def exists(self, id: str) -> bool:
        """Check if record exists"""
        return self.db.query(self.model).filter(self.model.id == id).first() is not None

    def get_recent(self, limit: int = 10) -> List[ModelType]:
        """Get most recently created records"""
        return (
            self.db.query(self.model)
            .order_by(desc(self.model.created_at))
            .limit(limit)
            .all()
        )

    def bulk_create(
        self, data_list: List[Dict[str, Any]], created_by: Optional[str] = None
    ) -> List[ModelType]:
        """Create multiple records at once"""
        instances = []
        for data in data_list:
            data["created_by"] = created_by
            data["updated_by"] = created_by
            instance = self.model(**data)
            instances.append(instance)

        self.db.add_all(instances)
        self.db.commit()

        # Refresh all instances to get generated IDs
        for instance in instances:
            self.db.refresh(instance)

        return instances

    def filter_by(self, **filters) -> List[ModelType]:
        """
        Filter records by multiple fields.
        Example: filter_by(status='active', priority='high')
        """
        query = self.db.query(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        return query.all()
