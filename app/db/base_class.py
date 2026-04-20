# app/db/base_class.py
"""
Import all models here for Alembic to detect them.
"""

from app.db.base import Base

# Import models
from app.models.user import User  # noqa
from app.models.role import Role  # noqa
from app.models.token import Token  # noqa