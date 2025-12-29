"""
Authentication Utilities
JWT token generation and password hashing.
"""

from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Note: bcrypt has a 72-byte password limit. Passwords are truncated if needed.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    # Truncate to 72 bytes to avoid bcrypt errors
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token data if valid, None otherwise
    """
    try:
        # Decode with audience validation disabled (we validate manually)
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"verify_aud": False},  # Disable audience validation
        )
        print(f"[DEBUG] JWT decoded successfully: {payload}")
        return payload
    except JWTError as e:
        print(f"[DEBUG] JWT decode error: {type(e).__name__}: {str(e)}")
        print(
            f"[DEBUG] Token (first 50 chars): {token[:50] if len(token) > 50 else token}"
        )
        print(f"[DEBUG] Using secret: {settings.jwt_secret_key[:20]}...")
        return None
