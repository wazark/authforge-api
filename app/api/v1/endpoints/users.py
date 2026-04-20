# app/api/v1/endpoints/users.py
"""
User endpoints.

Protected routes that require authentication.
"""

from fastapi import APIRouter, Depends

from app.core.security_dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
    }