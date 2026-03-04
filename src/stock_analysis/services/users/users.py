import logging
from uuid import UUID
from stock_analysis.schemas.user import (
    UserCreate,
    UserLoginRequest,
    UserUpdatePassword,
)
from sqlalchemy.orm import Session
from stock_analysis.repositories.user import UserRepository
from stock_analysis.core.exceptions import (
    UserHasNotFound,
    InvalidCredentialError,
)
from stock_analysis.core.security import verify_password
from stock_analysis.core.security import get_password_hash


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

    def get_user(self, id: UUID):
        user = self.repository.get_by_id(id)
        return user

    def update_password(self, id: UUID, data: UserUpdatePassword):
        user = self.get_user(id)
        if not user:
            raise UserHasNotFound()
        updated_data = data.model_dump(exclude_unset=True)
        old_password = updated_data["old_password"].get_secret_value()
        new_password = updated_data["new_password"].get_secret_value()
        if not verify_password(old_password, user.hashed_password):
            raise InvalidCredentialError("Your old password is incorrect")
        hashed_password = get_password_hash(new_password)
        return self.repository.update_user(user, {"hashed_password": hashed_password})

    def delete_user(self, id: UUID):
        user_deleted = self.repository.delete_user(id)
        return user_deleted
