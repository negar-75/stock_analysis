import logging
from uuid import UUID
from stock_analysis.api.schemas.user import UserCreate, UserLoginRequest
from sqlalchemy.orm import Session
from stock_analysis.repositories.user import UserRepository
from stock_analysis.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialError,
)
from stock_analysis.api.security import verify_password


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user(self, data: UserCreate):
        user = self.repository.create(data)
        logger.info(f"User {data.user_name} created")
        return user

    def authenticate_user(self, data: UserLoginRequest):
        user = self.repository.get_by_email(data.email)
        if not user or not verify_password(
            data.password.get_secret_value(),
            user.hashed_password,
        ):
            raise InvalidCredentialError("Invalid email or password")

        return user

    def delete_user(self, id: UUID):
        user_deleted = self.repository.delete_user(id)
        return user_deleted
