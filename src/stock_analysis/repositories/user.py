from sqlalchemy.orm import Session
from sqlalchemy import delete
from uuid import UUID
from stock_analysis.api.schemas.user import UserCreate, UserResponse
from stock_analysis.db.models import User
from stock_analysis.api.security import get_password_hash
from sqlalchemy.exc import IntegrityError
from stock_analysis.core.exceptions import UserAlreadyExistsError


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: UserCreate) -> User:
        plain_password = user_data.password_1.get_secret_value()
        hashed_password = get_password_hash(plain_password)
        try:
            new_user = User(
                user_name=user_data.user_name,
                phone=user_data.phone,
                email=user_data.email,
                hashed_password=hashed_password,
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsError()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, id: UUID):
        return self.db.query(User).filter(User.id == id).first()

    def delete_user(self, id: UUID):
        user = self.get_by_id(id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
