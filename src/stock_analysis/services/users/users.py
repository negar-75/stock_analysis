"""
User service for authentication and user management.

Handles user creation, authentication, password updates, and deletion.
"""

import logging
from uuid import UUID

from sqlalchemy.orm import Session

from stock_analysis.core.exceptions import InvalidCredentialError, UserNotFound
from stock_analysis.core.security import get_password_hash, verify_password
from stock_analysis.repositories.user import UserRepository
from stock_analysis.schemas.user import (
    UserCreate,
    UserLoginRequest,
    UserUpdatePassword,
)


logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user(self, data: UserCreate):
        """Create a new user with hashed password."""
        user = self.repository.create(data)
        logger.info("User %s created", data.user_name)
        return user

    def authenticate_user(self, data: UserLoginRequest):
        """Authenticate user by email and password. Raises InvalidCredentialError on failure."""
        user = self.repository.get_by_email(data.email)
        if not user or not verify_password(
            data.password.get_secret_value(),
            user.hashed_password,
        ):
            raise InvalidCredentialError("Invalid email or password")

        return user

    def get_user(self, user_id: UUID):
        """Fetch a user by ID. Returns None if not found."""
        return self.repository.get_by_id(user_id)

    def update_password(self, user_id: UUID, data: UserUpdatePassword):
        """Update user password. Raises UserNotFound or InvalidCredentialError on failure."""
        user = self.get_user(user_id)
        if not user:
            raise UserNotFound()
        updated_data = data.model_dump(exclude_unset=True)
        old_password = updated_data["old_password"].get_secret_value()
        new_password = updated_data["new_password"].get_secret_value()
        if not verify_password(old_password, user.hashed_password):
            raise InvalidCredentialError("Your old password is incorrect")
        hashed_password = get_password_hash(new_password)
        return self.repository.update_user(user, {"hashed_password": hashed_password})

    def delete_user(self, user_id: UUID):
        """Delete a user by ID. Returns False if user not found."""
        return self.repository.delete_user(user_id)
