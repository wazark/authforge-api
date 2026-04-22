#app/api/v1/endpoints/auth.py
"""
Authentication endpoints.

Handles user registration, login, refresh, and logout.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.models.user import User

from app.core.dependencies import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest
)

router = APIRouter()
security = HTTPBearer()

@router.post("/register", status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    try:
        service = UserService(db)
        user = service.create_user(data.email, data.password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    User login.
    """
    try:
        service = AuthService(db)
        tokens = service.login(data.email, data.password)
        return tokens
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@router.post("/refresh")
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token.
    """
    try:
        service = AuthService(db)
        return service.refresh(data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
def logout(
    data: RefreshTokenRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Logout user (revoke refresh + access token).
    """

    access_token = credentials.credentials

    service = AuthService(db)
    service.logout(data.refresh_token, access_token)

    return {"message": "Logged out successfully"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active
    }