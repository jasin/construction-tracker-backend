"""Utility functions for the application."""

from app.utils.auth import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)
from app.utils.exceptions import (
    ensure_exists,
    ensure_operation_success,
    raise_bad_request,
    raise_conflict,
    raise_forbidden,
    raise_not_found,
    raise_unauthorized,
)

__all__ = [
    # Auth utilities
    "create_access_token",
    "decode_access_token",
    "get_password_hash",
    "verify_password",
    # Error utilities
    "ensure_exists",
    "ensure_operation_success",
    "raise_bad_request",
    "raise_conflict",
    "raise_forbidden",
    "raise_not_found",
    "raise_unauthorized",
]
