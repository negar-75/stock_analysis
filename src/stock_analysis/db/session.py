from stock_analysis.db.engine import get_engine

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

engine = get_engine("prod")

SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
