"""
AuditLog model.

Stores security-relevant events for auditing purposes.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime, timezone

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # User associated with the event (nullable for anonymous events)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Action type (login, logout, refresh, etc.)
    action = Column(String, nullable=False, index=True)

    # Additional contextual information
    details = Column(JSON, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )