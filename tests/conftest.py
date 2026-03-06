import pytest
import pandas as pd
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from stock_analysis.db.models import Base
from stock_analysis.core.config import Settings


@pytest.fixture(scope="session")
async def test_engine():
    settings = Settings(_env_file=".env.test")

    engine = create_async_engine(settings.database_url)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="session")
async def test_setup_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_setup_session(test_engine, test_setup_db):
    SessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

    async with SessionLocal() as session:
        yield session


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
