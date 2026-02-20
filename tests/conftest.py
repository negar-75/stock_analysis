import pytest
import pandas as pd
from sqlalchemy.orm import sessionmaker
from stock_analysis.db.models.daily_prices import Base
from stock_analysis.db.engine import get_engine


@pytest.fixture(scope="session")
def test_engine():
    engine = get_engine("test")
    yield engine
    engine.dispose()


@pytest.fixture
def test_setup_db(test_engine):
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def test_setup_session(test_engine, test_setup_db):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def get_mock_price_data():
    """Factory that returns fresh DataFrame each call"""

    def _make_data():
        df = pd.DataFrame(
            {
                "Date": pd.date_range("2025-01-01", periods=10, freq="D"),
                "Ticker": ["AAPL"] * 10,
                "Open": [
                    100.0,
                    102.0,
                    101.0,
                    103.0,
                    104.0,
                    105.0,
                    107.0,
                    106.0,
                    108.0,
                    110.0,
                ],
                "High": [
                    103.0,
                    104.0,
                    103.0,
                    105.0,
                    106.0,
                    108.0,
                    109.0,
                    109.0,
                    111.0,
                    112.0,
                ],
                "Low": [
                    99.0,
                    100.0,
                    100.0,
                    101.0,
                    103.0,
                    104.0,
                    105.0,
                    105.0,
                    106.0,
                    108.0,
                ],
                "Close": [
                    102.0,
                    101.0,
                    103.0,
                    104.0,
                    105.0,
                    107.0,
                    106.0,
                    108.0,
                    110.0,
                    111.0,
                ],
                "Volume": [
                    1_000_000,
                    1_200_000,
                    950_000,
                    1_100_000,
                    1_050_000,
                    1_300_000,
                    1_250_000,
                    1_180_000,
                    1_400_000,
                    1_500_000,
                ],
            }
        )
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize("America/New_York")
        return df

    return _make_data
