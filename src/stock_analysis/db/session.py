from sqlalchemy.ext.asyncio import async_sessionmaker
from stock_analysis.db.engine import get_engine


SessionLocal = None


def get_session_maker():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = async_sessionmaker(
            bind=get_engine(),
            expire_on_commit=False,
        )
    return SessionLocal