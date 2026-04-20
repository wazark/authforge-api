"""
Token repository.

Handles database operations for refresh tokens.
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.models.token import Token


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, token: Token) -> Token:
        """
        Store a refresh token.
        """
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def get(self, token_str: str) -> Optional[Token]:
        """
        Retrieve a token by its value.
        """
        return self.db.query(Token).filter(Token.token == token_str).first()

    def revoke(self, token: Token) -> None:
        """
        Revoke a token (logout).
        """
        token.is_revoked = True
        self.db.commit()