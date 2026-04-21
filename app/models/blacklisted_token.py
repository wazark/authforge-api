"""
BlacklistedToken model.

Stores invalidated JWT tokens (access tokens).
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.db.base import Base


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)

    jti = Column(String, unique=True, nullable=False, index=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )