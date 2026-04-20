# app/core/auth.py
"""
Authentication dependencies.

Handles extracting and validating the current user from JWT.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_token_payload
from app.repositories.user_repository import UserRepository


# -----------------------------
# Security scheme (Bearer Token)
# -----------------------------
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Extract and validate current user from JWT token.
    """

    token = credentials.credentials

    try:
        payload = get_token_payload(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Validate token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Fetch user from DB
    repo = UserRepository(db)
    user = repo.get_by_id(int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user