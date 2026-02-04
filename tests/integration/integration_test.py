import pytest
from src.pipeline import run_pipeline
from src.db.models import DailyPrices
import pandas as pd
from sqlalchemy import func


DTYPES = {
    "Date": "datetime64[ns]",
    "Open": "float64",
    "High": "float64",
    "Low": "float64",
    "Close": "float64",
    "Volume": "int64",
}


@pytest.fixture
def get_mock_price_data():
    """Factory that returns fresh DataFrame each call"""

    def _make_data():
        return pd.DataFrame(
            {
                "Date": pd.date_range("2025-01-01", periods=10, freq="D"),
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

    return _make_data


def test_pipeline_inserted_rows(get_mock_price_data, test_engine, test_setup_session):
    inserted_rows = run_pipeline(DTYPES, get_mock_price_data(), test_engine)
    result = test_setup_session.query(DailyPrices).count()
    assert inserted_rows == result


def test_pipeline_null_count(
    get_mock_price_data, test_engine, test_setup_db, test_setup_session
):
    run_pipeline(DTYPES, get_mock_price_data(), test_engine)
    for col in ["date", "open", "high", "low", "close", "volume"]:
        column = getattr(DailyPrices, col)
        null_count = (
            test_setup_session.query(func.count()).filter(column.is_(None)).scalar()
        )
        assert null_count == 0, f"found {null_count} in {column}"


def test_pipeline_idempotency(get_mock_price_data, test_engine, test_setup_db):
    """Test pipeline doesn't insert duplicates on re-run"""
    first_run = run_pipeline(DTYPES, get_mock_price_data(), test_engine)
    second_run = run_pipeline(DTYPES, get_mock_price_data(), test_engine)

    assert first_run == 10
    assert second_run == 0
