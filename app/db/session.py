"""
Database session and engine configuration.

This module creates the SQLAlchemy engine and session factory
used across the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Create SQLAlchemy Engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Checks connections before using them
)


# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)