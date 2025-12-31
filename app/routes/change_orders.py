"""
Change Order Routes
API endpoints for change order management.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import ActivityLogRepository, ChangeOrderRepository
from app.schemas import (
    ChangeOrderCreateSchema,
    ChangeOrderListResponseSchema,
    ChangeOrderResponseSchema,
    ChangeOrderUpdateSchema,
)
from app.utils.dependencies import get_current_user
from app.utils.exceptions import (
    ensure_exists,
    ensure_operation_success,
    raise_bad_request,
)

router = APIRouter(prefix="/change-orders", tags=["change-orders"])


@router.get("", response_model=list[ChangeOrderListResponseSchema])
async def list_change_orders(
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    requested_by: Optional[str] = Query(None),
    approved_by: Optional[str] = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of change orders with optional filters."""
    co_repo = ChangeOrderRepository(db)

    if project_id and status:
        change_orders = co_repo.get_by_status(
            status, project_id=project_id, skip=skip, limit=limit
        )
    elif project_id:
        change_orders = co_repo.get_by_project_id(project_id, skip=skip, limit=limit)
    elif requested_by and status:
        change_orders = co_repo.get_by_requested_by(
            requested_by, status=status, skip=skip, limit=limit
        )
    elif requested_by:
        change_orders = co_repo.get_by_requested_by(
            requested_by, skip=skip, limit=limit
        )
    elif approved_by:
        change_orders = co_repo.get_by_approved_by(approved_by, skip=skip, limit=limit)
    elif status:
        change_orders = co_repo.get_by_status(status, skip=skip, limit=limit)
    else:
        change_orders = co_repo.get_all(skip=skip, limit=limit)

    return change_orders


@router.get("/pending-approval", response_model=list[ChangeOrderListResponseSchema])
async def list_pending_approval(
    project_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get change orders pending approval."""
    co_repo = ChangeOrderRepository(db)
    change_orders = co_repo.get_pending_approval(
        project_id=project_id, skip=skip, limit=limit
    )
    return change_orders


@router.get("/search", response_model=list[ChangeOrderListResponseSchema])
async def search_change_orders(
    q: str = Query(..., min_length=1, description="Search term"),
    project_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search change orders by title or description."""
    co_repo = ChangeOrderRepository(db)
    change_orders = co_repo.search_change_orders(
        q, project_id=project_id, skip=skip, limit=limit
    )
    return change_orders


@router.get("/total-cost/{project_id}")
async def get_total_cost(
    project_id: str,
    approved_only: bool = Query(False, description="Only count approved change orders"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get total cost of change orders for a project."""
    co_repo = ChangeOrderRepository(db)

    if approved_only:
        total = co_repo.get_approved_cost_by_project(project_id)
    else:
        total = co_repo.get_total_cost_by_project(project_id)

    return {
        "project_id": project_id,
        "total_cost": total,
        "approved_only": approved_only,
    }


@router.get("/{change_order_id}", response_model=ChangeOrderResponseSchema)
async def get_change_order(
    change_order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific change order by ID."""
    co_repo = ChangeOrderRepository(db)
    change_order = co_repo.get_by_id(change_order_id)

    ensure_exists(change_order, "Change order", change_order_id)

    return change_order


@router.post(
    "", response_model=ChangeOrderResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_change_order(
    co_data: ChangeOrderCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new change order."""
    co_repo = ChangeOrderRepository(db)
    activity_repo = ActivityLogRepository(db)

    change_order = co_repo.create(co_data.model_dump(), created_by=current_user.id)

    activity_repo.log_activity(
        project_id=change_order.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="change_order_created",
        entity_type="change_order",
        entity_id=change_order.id,
        description=f"Created change order: {change_order.title}",
        additional_data={"status": change_order.status, "cost": change_order.cost},
    )

    return change_order


@router.patch("/{change_order_id}", response_model=ChangeOrderResponseSchema)
async def update_change_order(
    change_order_id: str,
    co_data: ChangeOrderUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing change order."""
    co_repo = ChangeOrderRepository(db)
    activity_repo = ActivityLogRepository(db)

    ensure_exists(co_repo.get_by_id(change_order_id), "Log")

    change_order = ensure_operation_success(
        co_repo.update(
            change_order_id,
            co_data.model_dump(exclude_unset=True),
            updated_by=current_user.id,
        ),
        "update",
        "Change Order",
    )

    activity_repo.log_activity(
        project_id=change_order.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="change_order_updated",
        entity_type="change_order",
        entity_id=change_order.id,
        description=f"Updated change order: {change_order.title}",
        additional_data=co_data.model_dump(exclude_unset=True),
    )

    return change_order


@router.delete("/{change_order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_change_order(
    change_order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a change order."""
    co_repo = ChangeOrderRepository(db)
    activity_repo = ActivityLogRepository(db)

    change_order = ensure_exists(co_repo.get_by_id(change_order_id), "Change Order")

    activity_repo.log_activity(
        project_id=change_order.project_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action="change_order_deleted",
        entity_type="change_order",
        entity_id=change_order.id,
        description=f"Deleted change order: {change_order.title}",
        additional_data={"status": change_order.status, "cost": change_order.cost},
    )

    if not co_repo.delete(change_order_id):
        raise_bad_request("Failed to delete change order")
