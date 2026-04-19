"""
Token model placeholder (for refresh tokens / blacklist).
"""

from sqlalchemy import Column, Integer
from app.db.base import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)