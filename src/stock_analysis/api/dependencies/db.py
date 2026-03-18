from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from stock_analysis.db.session import get_session_maker


async def get_session():
    session_maker = get_session_maker()
    async with session_maker() as session:
        yield session