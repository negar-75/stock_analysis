from sqlalchemy import create_engine
from src.db.config import get_db_url


def get_engine(db_evn_key: str):
    """
    Create and return a SQLAlchemy engine for PostgreSQL.
    """
    engine = create_engine(get_db_url(db_evn_key))
    return engine
