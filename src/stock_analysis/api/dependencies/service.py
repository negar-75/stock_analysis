from fastapi import Depends
from sqlalchemy.orm import Session
from stock_analysis.api.dependencies.db import get_db
from stock_analysis.services.users.users import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
