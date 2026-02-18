from sqlalchemy.orm import Session
from typing import Generator
from src.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI.
    Yields a database session.
    """

    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    yield from get_db()
