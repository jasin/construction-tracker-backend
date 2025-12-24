"""
User Routes
API endpoints for user management and authentication.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories import UserRepository
from app.schemas import (
    MessageResponse,
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user_data.email} is already registered",
        )

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
    user = user_repo.get_by_email(login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Check if user is active
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

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


@auth_router.get("/debug-token")
async def debug_token(current_user: User = Depends(get_current_user)):
    """Debug endpoint to see JWT token claims."""
    # This is a bit hacky but works for debugging
    import inspect

    from fastapi import Request

    from app.utils.auth import decode_access_token
    from app.utils.dependencies import get_token_from_header

    frame = inspect.currentframe()
    request = None
    for frame_info in inspect.getouterframes(frame):
        for var_name, var_value in frame_info.frame.f_locals.items():
            if isinstance(var_value, Request):
                request = var_value
                break
        if request:
            break

    if request:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            decoded = decode_access_token(token)
            return {"decoded_token": decoded, "user": current_user.email}

    return {"error": "Could not extract token"}


@auth_router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: PasswordChangeSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change current user's password."""
    user_repo = UserRepository(db)

    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # Update password
    new_password_hash = get_password_hash(password_data.new_password)
    user_repo.update_password_hash(current_user.id, new_password_hash)

    return MessageResponse(message="Password changed successfully")


# User Management Routes


@router.get("", response_model=list[UserListResponseSchema])
async def list_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
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
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with ID: {user_id}",
        )

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
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with ID: {user_id}",
        )

    # Authorization: users can update themselves, admins can update anyone
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    # Non-admins cannot change their role or active status
    if current_user.role != "admin":
        if user_data.role is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change user roles",
            )
        if user_data.active is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change active status",
            )

    # If email is being updated, check for duplicates
    if user_data.email and user_data.email != existing_user.email:
        if user_repo.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_data.email} is already in use",
            )

    # Handle password update
    user_dict = user_data.model_dump(exclude_unset=True)
    if "password" in user_dict:
        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))

    # Update user
    user = user_repo.update(user_id, user_dict, user_id=current_user.id)

    return user


@router.post("/{user_id}/deactivate", response_model=MessageResponse)
async def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Deactivate a user account (admin only)."""
    user_repo = UserRepository(db)

    user = user_repo.deactivate_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with ID: {user_id}",
        )

    return MessageResponse(message=f"User {user_id} deactivated successfully")


@router.post("/{user_id}/activate", response_model=MessageResponse)
async def activate_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Activate a user account (admin only)."""
    user_repo = UserRepository(db)

    user = user_repo.activate_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with ID: {user_id}",
        )

    return MessageResponse(message=f"User {user_id} activated successfully")


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Delete a user (admin only)."""
    user_repo = UserRepository(db)

    # Check if user exists
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with ID: {user_id}",
        )

    # Prevent deleting yourself
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    # Delete user
    user_repo.delete(user_id)

    return MessageResponse(message=f"User {user_id} deleted successfully")
