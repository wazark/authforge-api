"""
Reusable FastAPI dependencies.

Includes database session dependency.
"""

from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Provides a database session to API routes.

    Ensures the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()