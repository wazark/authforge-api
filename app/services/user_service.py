"""
User service.

Contains business logic related to users.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        """
        existing_user = self.repo.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists")

        user = User(
            email=email,
            hashed_password=hash_password(password)
        )

        return self.repo.create(user)