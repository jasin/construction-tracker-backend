"""
Client Routes
API endpoints for client management.
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository
from app.repositories.client_repository import ClientRepository
from app.schemas.client import (
    ClientCreateSchema,
    ClientResponseSchema,
    ClientUpdateSchema,
)
from app.utils.dependencies import get_current_user
from app.utils.exceptions import (
    ensure_exists,
    ensure_operation_success,
    raise_bad_request,
    raise_conflict,
)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientResponseSchema])
async def list_clients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
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
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
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

    ensure_exists(client, "Client", client_id)

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
    activity_repo = ActivityLogRepository(db)

    # Check if client with same email already exists
    existing_client = client_repo.get_by_email(client_data.email)
    if existing_client:
        raise_conflict("Client", "email", client_data.email)

    # Create the client
    client = client_repo.create(
        data=client_data.model_dump(exclude_unset=True), created_by=current_user.id
    )

    # Log activity
    activity_repo.log_activity(
        project_id=None,
        user_id=current_user.id,
        user_name=current_user.name,
        action="client_created",
        entity_type="client",
        entity_id=client.id,
        description=f"Created client: {client.name}",
        additional_data={"email": client.email, "phone": client.phone},
    )

    return client


@router.patch("/{client_id}", response_model=ClientResponseSchema)
async def update_client(
    client_id: str,
    client_data: ClientUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing client."""
    client_repo = ClientRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if client exists
    existing_client = ensure_exists(
        client_repo.get_by_id(client_id), "Client", client_id
    )

    # Check if email is being changed to one that already exists
    if client_data.email and client_data.email != existing_client.email:
        email_check = client_repo.get_by_email(client_data.email)
        if email_check:
            raise_conflict("Client", "email", client_data.email)

    # Update the client
    updated_client = ensure_operation_success(
        client_repo.update(
            id=client_id,
            data=client_data.model_dump(exclude_unset=True),
            updated_by=current_user.id,
        ),
        "update",
        "Client",
    )

    # Log activity
    activity_repo.log_activity(
        project_id=None,
        user_id=current_user.id,
        user_name=current_user.name,
        action="client_updated",
        entity_type="client",
        entity_id=updated_client.id,
        description=f"Updated client: {updated_client.name}",
        additional_data=client_data.model_dump(exclude_unset=True),
    )

    return updated_client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a client."""
    client_repo = ClientRepository(db)
    activity_repo = ActivityLogRepository(db)

    # Check if client exists and get non-None reference
    client = ensure_exists(client_repo.get_by_id(client_id), "Client", client_id)

    # Log activity before deletion
    activity_repo.log_activity(
        project_id=None,
        user_id=current_user.id,
        user_name=current_user.name,
        action="client_deleted",
        entity_type="client",
        entity_id=client.id,
        description=f"Deleted client: {client.name}",
        additional_data={"email": client.email, "phone": client.phone},
    )

    # Delete client
    if not client_repo.delete(client_id):
        raise_bad_request("Failed to delete client")
