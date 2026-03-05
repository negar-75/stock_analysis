from stock_analysis.db.session import SessionLocal


from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.
    """
    async with SessionLocal() as session:
        yield session
