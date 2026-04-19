"""
User model placeholder.
Will be expanded in the next step.
"""

from sqlalchemy import Column, Integer
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)