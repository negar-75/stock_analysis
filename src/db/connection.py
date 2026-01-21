from sqlalchemy import create_engine
from src.db.config import get_db_url
from sqlalchemy.orm import sessionmaker


def get_engine():
    """
    Create and return a SQLAlchemy engine for PostgreSQL.
    """
    engine = create_engine(get_db_url())
    return engine


engine = get_engine()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
