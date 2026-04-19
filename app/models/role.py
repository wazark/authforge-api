"""
Role model placeholder.
"""

from sqlalchemy import Column, Integer
from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)