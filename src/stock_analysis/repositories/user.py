from sqlalchemy.orm import Session
from stock_analysis.api.schemas.user import UserCreate
from stock_analysis.db.models import User
from stock_analysis.db.session import SessionLocal
from stock_analysis.api.security import get_password_hash


class UserRepositiry:
    def __init__(self, db: Session):
        self.db = db

    def user_create(self, user_data: UserCreate):
        plain_password = user_data.password_1.get_secret_value()
        hashed_password = get_password_hash(plain_password)
        try:
            new_user = User(
                username=user_data.user_name,
                phone=user_data.phone,
                email=user_data.email,
                hashed_password=hashed_password,
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except Exception as e:
            self.db.rollback()
            raise e

        # Todo continue creating CRUD class for user


# user = UserCreate(
#     user_name="negar",
#     email="nasirinegar13@gmail.com",
#     phone="0915582567",
#     password_1="123456789012",
#     password_2="123456789012",
# )


# with SessionLocal() as db:
#     data = UserRepositiry(db)
#     user = data.user_create(user_data=user)
#     print(user)
