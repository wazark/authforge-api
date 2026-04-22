#app/repositories/user_repository.py
"""
User repository.

Handles database operations related to users.
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email.
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: User) -> User:
        """
        Create a new user.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user