#app/db/base_class.py
"""
Central import of all models.

This ensures SQLAlchemy metadata is aware of all tables.
"""

from app.db.base import Base

# Import all models here
from app.models.user import User  # noqa
from app.models.role import Role  # noqa
from app.models.token import Token  # noqa
from app.models.blacklisted_token import BlacklistedToken  # noqa