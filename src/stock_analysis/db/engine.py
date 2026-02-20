from sqlalchemy import create_engine
from stock_analysis.db.config import get_db_url


def get_engine(env: str):
    """
    Create and return a SQLAlchemy engine for PostgreSQL.
    """
    engine = create_engine(get_db_url(env))
    return engine
