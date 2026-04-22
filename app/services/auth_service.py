#app/services/auth_service.py
"""
Authentication service.

Handles login, token generation, and authentication logic.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.models.token import Token
from app.core.config import settings

from app.core.security import decode_token
from app.repositories.blacklist_repository import BlacklistRepository


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)

    def authenticate_user(self, email: str, password: str):
        """
        Validate user credentials.
        """
        user = self.user_repo.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def login(self, email: str, password: str):
        """
        Perform login and return tokens.
        """
        user = self.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid credentials")

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        # Store refresh token in DB
        token_obj = Token(
            token=refresh_token,
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        self.token_repo.create(token_obj)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh(self, refresh_token: str):
        """
        Refresh access token.
        """
        token = self.token_repo.get(refresh_token)

        if not token or token.is_revoked:
            raise ValueError("Invalid refresh token")

        if token.expires_at < datetime.now(timezone.utc):
            raise ValueError("Token expired")

        new_access_token = create_access_token(subject=token.user_id)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    def logout(self, refresh_token: str, access_token: str):
        """
        Revoke refresh token AND blacklist access token.
        """

        
        # Revoke refresh token
        token = self.token_repo.get(refresh_token)

        if token:
            self.token_repo.revoke(token)

        
        # Blacklist ACCESS token
        try:
            payload = decode_token(access_token)
            jti = payload.get("jti")

            if jti:
                blacklist = BlacklistRepository(self.token_repo.db)
                blacklist.add(jti)

        except Exception:
            pass  # avoid breaking logout