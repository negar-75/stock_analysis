from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from stock_analysis.api.dependencies.db import get_db
from stock_analysis.services.users.users_service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)
