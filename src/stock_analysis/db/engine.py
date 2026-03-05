from sqlalchemy.ext.asyncio import create_async_engine

from stock_analysis.db.config import get_db_url


def get_engine(env: str):
    """
    Create and return a SQLAlchemy engine for PostgreSQL.
    """
    return create_async_engine(get_db_url(env))
