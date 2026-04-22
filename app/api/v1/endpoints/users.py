#app/api/v1/endpoints/users.py
"""
User endpoints.

Protected routes that require authentication.
"""

from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.permissions import require_role


router = APIRouter()


@router.get("/me")
def get_me(current_user: User = Depends(require_role("user"))):
    """
    Get current authenticated user.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
    }

@router.get("/admin-only")
def admin_only(current_user: User = Depends(require_role("admin"))):
    return {"message": "Welcome, admin!"}