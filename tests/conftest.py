import asyncio
import os
import pandas as pd
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from fastapi import Request
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from stock_analysis.main import app
from stock_analysis.db import Base
from stock_analysis.api.dependencies.db import get_session
from stock_analysis.api.dependencies.rate_limiter import rate_limiter

load_dotenv(".env.test")

if os.getenv("POSTGRES_HOST") and os.getenv("POSTGRES_HOST") not in (
    "localhost",
    "127.0.0.1",
):
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "stock_analysis_test")
    user = os.getenv("POSTGRES_USER", "stock_user_test")
    password = os.getenv("POSTGRES_PASSWORD", "7648")
    DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
else:
    DATABASE_URL = (
        "postgresql+asyncpg://stock_user_test:7648@localhost:5432/stock_analysis_test"
    )



@pytest_asyncio.fixture(scope="session")
async def engine():
    # NullPool prevents connection reuse across async operations, avoiding
    # "another operation is in progress" errors with asyncpg in Docker/CI.
    _engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
    yield _engine
    await _engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def setup_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session(engine, setup_db):
    async with engine.connect() as conn:
        await conn.begin()
        async_session = async_sessionmaker(
            bind=conn,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        async with async_session() as s:
            yield s
        await conn.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_client(session):
    async def override_get_session():
        yield session

    async def noop_rate_limiter(request: Request):
        pass

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[rate_limiter] = noop_rate_limiter

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


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
