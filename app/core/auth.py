#app/core/auth.py
"""
Authentication dependencies.

Handles current user extraction from JWT.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import decode_token, validate_token_type
from app.repositories.user_repository import UserRepository
from app.repositories.blacklist_repository import BlacklistRepository

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Extract and validate current user from access token.
    """

    token = credentials.credentials

    try:
        payload = decode_token(token)

        # Validate token type
        validate_token_type(payload, "access")

        # Extract user ID
        user_id = int(payload.get("sub"))

        # Extract JTI
        jti = payload.get("jti")

        # Check blacklist
        blacklist = BlacklistRepository(db)

        if blacklist.exists(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revoked"
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # Fetch user
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user