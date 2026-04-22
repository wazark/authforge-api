#app/repositories/blacklist_repository.py
"""
Blacklist repository.

Handles blacklisted JWT tokens.
"""

from sqlalchemy.orm import Session

from app.models.blacklisted_token import BlacklistedToken


class BlacklistRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, jti: str):
        token = BlacklistedToken(jti=jti)
        self.db.add(token)
        self.db.commit()

    def exists(self, jti: str) -> bool:
        return self.db.query(BlacklistedToken).filter_by(jti=jti).first() is not None