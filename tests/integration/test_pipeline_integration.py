import pytest
import pandas as pd
from sqlalchemy import func
from stock_analysis.core.pipeline_config import DTYPES
from stock_analysis.pipelines.orchestrators.stock_pipeline import StockDataPipeline
from stock_analysis.db.models.daily_prices import DailyPrices


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


def test_stock_pipeline_full_run(get_mock_price_data):
    pipeline = StockDataPipeline(
        dtypes=DTYPES,
        raw_data=get_mock_price_data(),
        volatility_window=3,
        moving_window=3,
    )

    result = pipeline.run()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 10

    expected_columns = {
        "ticker",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "daily_return",
        "log_return",
        "rolling_volatility",
        "moving_average",
        "absolute_range",
        "relative_range_on_open",
        "relative_range_on_close",
        "open_close_range",
        "upper_shadow",
        "lower_shadow",
    }

    assert expected_columns.issubset(set(result.columns))


def test_stock_pipeline_feature_values(get_mock_price_data):
    pipeline = StockDataPipeline(DTYPES, get_mock_price_data(), 3, 3)
    df = pipeline.run()

    # first row return should be NaN
    assert pd.isna(df.loc[0, "daily_return"])

    # absolute range = high - low
    assert df.loc[1, "absolute_range"] == pytest.approx(
        df.loc[1, "high"] - df.loc[1, "low"]
    )

    # open_close_range = close - open
    assert df.loc[2, "open_close_range"] == pytest.approx(
        df.loc[2, "close"] - df.loc[2, "open"]
    )


def test_stock_pipeline_validation_error(get_mock_price_data):
    df = get_mock_price_data()

    # break validation → remove column
    df = df.drop(columns=["High"])

    pipeline = StockDataPipeline(DTYPES, df, 3, 3)

    with pytest.raises(ValueError, match="Validation failed"):
        pipeline.run()
