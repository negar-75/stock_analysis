from sqlalchemy.orm import Session
from uuid import UUID
from stock_analysis.schemas.user import UserCreate
from stock_analysis.db.models import User
from stock_analysis.core.security import get_password_hash
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

    def update_user(self, user: User, data: dict):
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, id: UUID):
        user = self.get_by_id(id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
