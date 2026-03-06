from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from stock_analysis.schemas.user import UserCreate
from stock_analysis.db.models import User
from stock_analysis.core.security import get_password_hash
from stock_analysis.core.exceptions import UserAlreadyExistsError


class UserRepository:
    """Repository for user CRUD operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user. Raises UserAlreadyExistsError on duplicate email/username."""

        user = await self.get_by_email(user_data.email)
        if user:
            raise UserAlreadyExistsError()
        plain_password = user_data.password_1.get_secret_value()
        hashed_password = get_password_hash(plain_password)

        new_user = User(
            user_name=user_data.user_name,
            phone=user_data.phone,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        try:
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user

        except IntegrityError:
            await self.db.rollback()
            raise UserAlreadyExistsError()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Fetch a user by UUID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user: User, data: dict) -> User:
        for key, value in data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user by UUID."""

        user = await self.get_by_id(user_id)

        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()

        return True
