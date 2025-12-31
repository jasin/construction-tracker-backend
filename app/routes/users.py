"""
User Routes
API endpoints for user management and authentication.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import UserRepository
from app.schemas import (
    PasswordChangeSchema,
    UserCreateSchema,
    UserListResponseSchema,
    UserLoginResponseSchema,
    UserLoginSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from app.utils.auth import create_access_token, get_password_hash, verify_password
from app.utils.dependencies import get_current_user, require_admin
from app.utils.exceptions import (
    ensure_exists,
    ensure_operation_success,
    raise_bad_request,
    raise_forbidden,
    raise_not_found,
    raise_unauthorized,
)

router = APIRouter(prefix="/users", tags=["users"])
auth_router = APIRouter(prefix="/auth", tags=["authentication"])


# Authentication Routes


@auth_router.post(
    "/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    """Register a new user."""
    user_repo = UserRepository(db)

    # Check if email already exists
    if user_repo.email_exists(user_data.email):
        raise_bad_request(f"Email {user_data.email} is already registered")

    # Hash password
    user_dict = user_data.model_dump()
    user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))

    # Create user
    user = user_repo.create(user_dict)

    return user


@auth_router.post("/login", response_model=UserLoginResponseSchema)
async def login(login_data: UserLoginSchema, db: Session = Depends(get_db)):
    """Login and get access token."""
    user_repo = UserRepository(db)

    # Get user by email
    user = ensure_exists(user_repo.get_by_email(login_data.email), "Email")

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise_unauthorized("Incorrect email or password")

    # Check if user is active
    if not user.active:
        raise_forbidden("User account is inactive")

    # Create access token with Supabase-compatible claims
    # Supabase requires: aud, iss, sub, role, exp
    access_token = create_access_token(
        data={
            "aud": "authenticated",  # REQUIRED: Audience claim
            "iss": "https://pjtltwthpeufcfmewfsx.supabase.co/auth/v1",  # REQUIRED: Issuer (Supabase auth URL)
            "role": "authenticated",  # REQUIRED: Role for RLS policies
            "sub": user.id,  # REQUIRED: Subject (user ID)
            "email": user.email,
            "user_metadata": {
                "name": user.name,
                "app_role": user.role,  # Your app's custom role
            },
        }
    )

    return UserLoginResponseSchema(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        token=access_token,
        token_type="bearer",
        created_at=user.created_at,
        updated_at=user.updated_at,
        created_by=user.created_by,
        updated_by=user.updated_by,
    )


@auth_router.get("/me", response_model=UserResponseSchema)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@auth_router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    password_data: PasswordChangeSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change current user's password."""
    user_repo = UserRepository(db)

    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise_bad_request("Current password is incorrect")

    # Update password
    new_password_hash = get_password_hash(password_data.new_password)
    if not user_repo.update_password_hash(current_user.id, new_password_hash):
        raise_bad_request("Failed to update password")


# User Management Routes


@router.get("", response_model=list[UserListResponseSchema])
async def list_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of users with optional filters."""
    user_repo = UserRepository(db)

    if role:
        users = user_repo.get_by_role(role, skip=skip, limit=limit)
    elif active is not None:
        if active:
            users = user_repo.get_active_users(skip=skip, limit=limit)
        else:
            users = user_repo.get_inactive_users(skip=skip, limit=limit)
    else:
        users = user_repo.get_all(skip=skip, limit=limit)

    return users


@router.get("/search", response_model=list[UserListResponseSchema])
async def search_users(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search users by name or email."""
    user_repo = UserRepository(db)
    users = user_repo.search_users(q, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific user by ID."""
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise_not_found(f"User not found with ID: {user_id}")

    return user


@router.patch("/{user_id}", response_model=UserResponseSchema)
async def update_user(
    user_id: str,
    user_data: UserUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a user. Users can update themselves, admins can update anyone."""
    user_repo = UserRepository(db)

    # Check if user exists
    existing_user = ensure_exists(user_repo.get_by_id(user_id), "User", user_id)

    # Authorization: users can update themselves, admins can update anyone
    if current_user.id != user_id and current_user.role != "admin":
        raise_forbidden("Not authorized to update this user")

    # Non-admins cannot change their role or active status
    if current_user.role != "admin":
        if user_data.role is not None:
            raise_forbidden("Only admins can change user roles")
        if user_data.active is not None:
            raise_forbidden("Only admins can change active status")

    # If email is being updated, check for duplicates
    if user_data.email and user_data.email != existing_user.email:
        if user_repo.email_exists(user_data.email):
            raise_bad_request("Email {user_data.email} is already in use")

    # Handle password update
    user_dict = user_data.model_dump(exclude_unset=True)
    if "password" in user_dict:
        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))

    # Update user
    user = user_repo.update(user_id, user_dict, updated_by=current_user.id)

    return user


@router.post("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Deactivate a user account (admin only)."""
    user_repo = UserRepository(db)

    ensure_operation_success(user_repo.deactivate_user(user_id), "deactivate", "User")


@router.post("/{user_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Activate a user account (admin only)."""
    user_repo = UserRepository(db)

    ensure_operation_success(user_repo.activate_user(user_id), "activate", "User")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Delete a user (admin only)."""
    user_repo = UserRepository(db)

    # Check if user exists
    ensure_exists(user_repo.get_by_id(user_id), "User", user_id)

    # Prevent deleting yourself
    if user_id == admin_user.id:
        raise_bad_request("Cannot delete your own account")

    # Delete user
    if not user_repo.delete(user_id):
        raise_bad_request("Failed to delete user")
