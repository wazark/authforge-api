#app/core/permissions.py
"""
Authorization utilities.

Provides role-based access control (RBAC) dependencies.
"""

from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.core.auth import get_current_user


def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):

        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned"
            )

        if current_user.role.name != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_user

    return role_checker