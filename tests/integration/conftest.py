from src.db.engine import get_engine, get_db
import pytest
from src.db.models.daily_prices import Base
from sqlalchemy import inspect


@pytest.fixture(scope="session")
def test_engine():
    engine = get_engine("DB_NAME_TEST")
    yield engine
    engine.dispose()


@pytest.fixture
def test_setup_db(test_engine):
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def test_setup_session(test_engine, test_setup_db):
    session = get_db(test_engine)
    try:
        yield session
        session.commit()
    finally:
        session.close()
