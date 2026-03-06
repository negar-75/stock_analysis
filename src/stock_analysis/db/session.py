from stock_analysis.db.engine import engine

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
