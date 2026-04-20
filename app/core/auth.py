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

        # 🔐 Ensure this is an ACCESS token
        validate_token_type(payload, "access")

        user_id = int(payload.get("sub"))

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user