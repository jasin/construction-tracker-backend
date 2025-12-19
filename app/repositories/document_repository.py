"""
Document Repository
Provides data access operations for Document entities.
"""

from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """Repository for Document-specific database operations."""

    def __init__(self, db: Session):
        super().__init__(Document, db)

    def get_by_project_id(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Document]:
        """
        Get all documents for a specific project.

        Args:
            project_id: The project ID to filter by
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of Document objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type(
        self,
        doc_type: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        """
        Get documents by type, optionally filtered by project.

        Args:
            doc_type: Document type to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Document objects
        """
        query = self.db.query(self.model).filter(self.model.type == doc_type)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_category(
        self,
        category: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        """
        Get documents by category, optionally filtered by project.

        Args:
            category: Document category to filter by
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Document objects
        """
        query = self.db.query(self.model).filter(self.model.category == category)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_linked_entity(
        self, linked_entity_id: str, skip: int = 0, limit: int = 100
    ) -> List[Document]:
        """
        Get all documents linked to a specific entity (task, RFI, submittal, etc.).

        Args:
            linked_entity_id: The entity ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Document objects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.linked_entity_id == linked_entity_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_uploaded_by(
        self,
        user_id: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        """
        Get documents uploaded by a specific user.

        Args:
            user_id: User ID who uploaded the document
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Document objects
        """
        query = self.db.query(self.model).filter(self.model.uploaded_by == user_id)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def search_documents(
        self,
        search_term: str,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        """
        Search documents by name.

        Args:
            search_term: Term to search for in document name
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching Document objects
        """
        search_pattern = f"%{search_term}%"
        query = self.db.query(self.model).filter(self.model.name.ilike(search_pattern))

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
    ) -> List[Document]:
        """
        Get documents uploaded within a date range.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Document objects within the date range
        """
        query = self.db.query(self.model)

        if start_date:
            query = query.filter(self.model.uploaded_date >= start_date)

        if end_date:
            query = query.filter(self.model.uploaded_date <= end_date)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_by_size_range(
        self,
        min_size: Optional[int] = None,
        max_size: Optional[int] = None,
        project_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        """
        Get documents within a size range.

        Args:
            min_size: Minimum file size in bytes
            max_size: Maximum file size in bytes
            project_id: Optional project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Document objects within the size range
        """
        query = self.db.query(self.model)

        if min_size is not None:
            query = query.filter(self.model.size >= min_size)

        if max_size is not None:
            query = query.filter(self.model.size <= max_size)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    def get_total_storage_by_project(self, project_id: str) -> int:
        """
        Calculate total storage used by documents for a project.

        Args:
            project_id: The project ID to calculate for

        Returns:
            Total storage in bytes (0 if none)
        """
        from sqlalchemy import func

        result = (
            self.db.query(func.sum(self.model.size))
            .filter(self.model.project_id == project_id)
            .scalar()
        )

        return result if result is not None else 0

    def get_document_count_by_type(self, project_id: str) -> dict:
        """
        Get count of documents by type for a project.

        Args:
            project_id: The project ID to analyze

        Returns:
            Dictionary mapping document types to counts
        """
        from sqlalchemy import func

        results = (
            self.db.query(self.model.type, func.count(self.model.id))
            .filter(self.model.project_id == project_id)
            .group_by(self.model.type)
            .all()
        )

        return {doc_type: count for doc_type, count in results}

    def get_document_count_by_category(self, project_id: str) -> dict:
        """
        Get count of documents by category for a project.

        Args:
            project_id: The project ID to analyze

        Returns:
            Dictionary mapping categories to counts
        """
        from sqlalchemy import func

        results = (
            self.db.query(self.model.category, func.count(self.model.id))
            .filter(self.model.project_id == project_id)
            .group_by(self.model.category)
            .all()
        )

        return {category: count for category, count in results}
