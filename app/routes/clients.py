"""
Client Routes
API endpoints for client management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories.client_repository import ClientRepository
from app.schemas.base import MessageResponse
from app.schemas.client import (
    ClientCreateSchema,
    ClientResponseSchema,
    ClientUpdateSchema,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientResponseSchema])
async def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of all clients."""
    client_repo = ClientRepository(db)
    clients = client_repo.get_all(skip=skip, limit=limit)
    return clients


@router.get("/search", response_model=list[ClientResponseSchema])
async def search_clients(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search clients by name."""
    client_repo = ClientRepository(db)
    clients = client_repo.search_by_name(q)
    return clients[skip : skip + limit]


@router.get("/{client_id}", response_model=ClientResponseSchema)
async def get_client(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific client by ID."""
    client_repo = ClientRepository(db)
    client = client_repo.get_by_id(client_id)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found",
        )

    return client


@router.post(
    "", response_model=ClientResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_client(
    client_data: ClientCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new client."""
    client_repo = ClientRepository(db)

    # Check if client with same email already exists
    if client_data.email:
        existing_client = client_repo.get_by_email(client_data.email)
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client with email {client_data.email} already exists",
            )

    # Create the client
    client = client_repo.create(
        data=client_data.model_dump(exclude_unset=True), created_by=current_user.id
    )

    return client


@router.put("/{client_id}", response_model=ClientResponseSchema)
async def update_client(
    client_id: str,
    client_data: ClientUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing client."""
    client_repo = ClientRepository(db)

    # Check if client exists
    existing_client = client_repo.get_by_id(client_id)
    if not existing_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found",
        )

    # Check if email is being changed to one that already exists
    if client_data.email and client_data.email != existing_client.email:
        email_check = client_repo.get_by_email(client_data.email)
        if email_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client with email {client_data.email} already exists",
            )

    # Update the client
    updated_client = client_repo.update(
        id=client_id,
        data=client_data.model_dump(exclude_unset=True),
        updated_by=current_user.id,
    )

    return updated_client


@router.delete("/{client_id}", response_model=MessageResponse)
async def delete_client(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a client."""
    client_repo = ClientRepository(db)

    success = client_repo.delete(client_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found",
        )

    return MessageResponse(message=f"Client {client_id} deleted successfully")
