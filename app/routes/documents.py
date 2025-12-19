"""
Document Routes
API endpoints for document management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository, DocumentRepository
from app.schemas import (
    DocumentCreateSchema,
    DocumentListResponseSchema,
    DocumentResponseSchema,
    DocumentUpdateSchema,
    MessageResponse,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[DocumentListResponseSchema])
async def list_documents(
    project_id: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    linked_entity_id: Optional[str] = Query(None),
    uploaded_by: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of documents with optional filters."""
    doc_repo = DocumentRepository(db)

    if linked_entity_id:
        documents = doc_repo.get_by_linked_entity(
            linked_entity_id, skip=skip, limit=limit
        )
    elif project_id and type:
        documents = doc_repo.get_by_type(
            type, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id and category:
        documents = doc_repo.get_by_category(
            category, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id and uploaded_by:
        documents = doc_repo.get_by_uploaded_by(
            uploaded_by, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id:
        documents = doc_repo.get_by_project_id(project_id, skip=skip, limit=limit)
    elif type:
        documents = doc_repo.get_by_type(type, skip=skip, limit=limit)
    elif category:
        documents = doc_repo.get_by_category(category, skip=skip, limit=limit)
    elif uploaded_by:
        documents = doc_repo.get_by_uploaded_by(uploaded_by, skip=skip, limit=limit)
    else:
        documents = doc_repo.get_all(skip=skip, limit=limit)

    return documents


@router.get("/search", response_model=list[DocumentListResponseSchema])
async def search_documents(
    q: str = Query(..., min_length=1),
    project_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search documents by name."""
    doc_repo = DocumentRepository(db)
    documents = doc_repo.search_documents(
        q, project_id=project_id, skip=skip, limit=limit
    )
    return documents


@router.get("/storage/{project_id}")
async def get_storage_usage(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get total storage used by documents for a project."""
    doc_repo = DocumentRepository(db)
    total_bytes = doc_repo.get_total_storage_by_project(project_id)
    total_mb = total_bytes / (1024 * 1024)

    return {
        "project_id": project_id,
        "total_bytes": total_bytes,
        "total_mb": round(total_mb, 2),
    }


@router.get("/stats/{project_id}")
async def get_document_stats(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get document statistics for a project."""
    doc_repo = DocumentRepository(db)

    by_type = doc_repo.get_document_count_by_type(project_id)
    by_category = doc_repo.get_document_count_by_category(project_id)
    total_storage = doc_repo.get_total_storage_by_project(project_id)

    return {
        "project_id": project_id,
        "count_by_type": by_type,
        "count_by_category": by_category,
        "total_storage_bytes": total_storage,
        "total_storage_mb": round(total_storage / (1024 * 1024), 2),
    }


@router.get("/{document_id}", response_model=DocumentResponseSchema)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific document by ID."""
    doc_repo = DocumentRepository(db)
    document = doc_repo.get_by_id(document_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document not found with ID: {document_id}",
        )

    return document


@router.post(
    "", response_model=DocumentResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_document(
    doc_data: DocumentCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new document record."""
    doc_repo = DocumentRepository(db)
    activity_repo = ActivityLogRepository(db)

    document = doc_repo.create(doc_data.model_dump(), user_id=current_user.id)

    activity_repo.log_activity(
        project_id=document.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="document_uploaded",
        entity_type="document",
        entity_id=document.id,
        description=f"Uploaded document: {document.name}",
        additional_data={"category": document.category, "type": document.type},
    )

    return document


@router.patch("/{document_id}", response_model=DocumentResponseSchema)
async def update_document(
    document_id: str,
    doc_data: DocumentUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing document record."""
    doc_repo = DocumentRepository(db)
    activity_repo = ActivityLogRepository(db)

    existing_doc = doc_repo.get_by_id(document_id)
    if not existing_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document not found with ID: {document_id}",
        )

    document = doc_repo.update(
        document_id, doc_data.model_dump(exclude_unset=True), user_id=current_user.id
    )

    activity_repo.log_activity(
        project_id=document.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="document_updated",
        entity_type="document",
        entity_id=document.id,
        description=f"Updated document: {document.name}",
        additional_data=doc_data.model_dump(exclude_unset=True),
    )

    return document


@router.delete("/{document_id}", response_model=MessageResponse)
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a document record."""
    doc_repo = DocumentRepository(db)
    activity_repo = ActivityLogRepository(db)

    document = doc_repo.get_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document not found with ID: {document_id}",
        )

    activity_repo.log_activity(
        project_id=document.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="document_deleted",
        entity_type="document",
        entity_id=document.id,
        description=f"Deleted document: {document.name}",
        additional_data={"category": document.category, "type": document.type},
    )

    doc_repo.delete(document_id)

    return MessageResponse(message=f"Document {document_id} deleted successfully")
