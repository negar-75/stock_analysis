from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from stock_analysis.db.session import get_session_maker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = get_session_maker()

    async with SessionLocal() as session:
        yield session
