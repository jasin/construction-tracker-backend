"""
Error handling utilities for consistent API error responses.

This module provides helper functions to raise HTTPExceptions with
consistent formatting and messaging across the API.
"""

from typing import Any, Optional

from fastapi import HTTPException, status


def raise_not_found(entity_type: str, entity_id: Optional[str] = None) -> None:
    """
    Raise a 404 Not Found error with consistent formatting.

    Args:
        entity_type: Type of entity (e.g., "RFI", "Project", "Task")
        entity_id: Optional ID of the entity that wasn't found

    Raises:
        HTTPException: 404 Not Found

    Example:
        raise_not_found("RFI", rfi_id)
        # Raises: HTTPException(404, "RFI not found with ID: abc123")

        raise_not_found("User")
        # Raises: HTTPException(404, "User not found")
    """
    if entity_id:
        detail = f"{entity_type} not found with ID: {entity_id}"
    else:
        detail = f"{entity_type} not found"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def raise_bad_request(message: str) -> None:
    """
    Raise a 400 Bad Request error.

    Args:
        message: Error message describing what went wrong

    Raises:
        HTTPException: 400 Bad Request

    Example:
        raise_bad_request("Failed to update RFI")
    """
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


def raise_unauthorized(message: str = "Unauthorized") -> None:
    """
    Raise a 401 Unauthorized error.

    Args:
        message: Error message (default: "Unauthorized")

    Raises:
        HTTPException: 401 Unauthorized
    """
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


def raise_forbidden(message: str = "Forbidden") -> None:
    """
    Raise a 403 Forbidden error.

    Args:
        message: Error message (default: "Forbidden")

    Raises:
        HTTPException: 403 Forbidden
    """
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)


def raise_conflict(entity_type: str, field: str, value: Any) -> None:
    """
    Raise a 409 Conflict error (e.g., duplicate entries).

    Args:
        entity_type: Type of entity (e.g., "User", "Project")
        field: Field that conflicts (e.g., "email", "job_number")
        value: The conflicting value

    Raises:
        HTTPException: 409 Conflict

    Example:
        raise_conflict("User", "email", user_data.email)
        # Raises: HTTPException(409, "User with email 'test@example.com' already exists")
    """
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{entity_type} with {field} '{value}' already exists",
    )


def ensure_exists(
    entity: Optional[Any], entity_type: str, entity_id: Optional[str] = None
) -> Any:
    """
    Ensure an entity exists, raise 404 if it doesn't.

    This is a convenience function that combines None checking with raising
    the appropriate error. It also provides type narrowing for type checkers.

    Args:
        entity: The entity to check (typically from repository query)
        entity_type: Type of entity for error message
        entity_id: Optional ID for error message

    Returns:
        The entity if it exists (guaranteed non-None)

    Raises:
        HTTPException: 404 Not Found if entity is None

    Example:
        rfi = rfi_repo.get_by_id(rfi_id)
        ensure_exists(rfi, "RFI", rfi_id)
        # After this line, type checkers know rfi is not None
        print(rfi.title)  # Safe to access
    """
    if entity is None:
        raise_not_found(entity_type, entity_id)
    return entity


def ensure_operation_success(
    entity: Optional[Any], operation: str, entity_type: str
) -> Any:
    """
    Ensure a repository operation succeeded, raise 400 if it didn't.

    Use this for operations that return Optional[Entity] (like create, update).

    Args:
        entity: Result of the operation (None indicates failure)
        operation: Operation name (e.g., "create", "update")
        entity_type: Type of entity

    Returns:
        The entity if operation succeeded (guaranteed non-None)

    Raises:
        HTTPException: 400 Bad Request if entity is None

    Example:
        rfi = ensure_operation_success(rfi_repo.update(rfi_id, data), "update", "RFI")
    """
    if entity is None:
        raise_bad_request(f"Failed to {operation} {entity_type}")
    return entity
