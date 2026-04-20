# app/db/init_db.py
"""
Initial database setup.

Creates default roles.
"""

from sqlalchemy.orm import Session
from app.models.role import Role


def init_db(db: Session):
    """
    Seed initial roles.
    """

    roles = ["admin", "user"]

    for role_name in roles:
        existing = db.query(Role).filter(Role.name == role_name).first()
        if not existing:
            role = Role(name=role_name)
            db.add(role)

    db.commit()