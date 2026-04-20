# app/db/base.py
"""
Base model for all SQLAlchemy models.

All database models should inherit from this Base class.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so Alembic can detect them
from app.models.user import User  # noqa
from app.models.role import Role  # noqa
from app.models.token import Token  # noqa