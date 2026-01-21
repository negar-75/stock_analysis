from src.helpers.features.features import FeatureEngineering
import pandas as pd
import numpy as np
import pytest


@pytest.fixture
def sample_ohlc_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [10.510000228881836, 10.0, 9.65999984741211],
            "high": [10.710000038146973, 10.050000190734863, 10.0],
            "low": [9.81999969482422, 9.75, 9.430000305175781],
            "close": [10.0, 9.75, 9.84000015258789],
            "adj_close": [10.0, 9.75, 9.84000015258789],
            "volume": [5412800, 918900, 1020000],
        }
    )


@pytest.fixture
def analyzed_data(sample_ohlc_data) -> pd.DataFrame:
    fe = FeatureEngineering(sample_ohlc_data, volatility_window=2, moving_window=2)
    return fe.run()


class TestNaNBehavior:
    def test_first_row_for_nan_returns(self, analyzed_data):
        assert pd.isna(analyzed_data.loc[0, ["daily_return", "log_return"]]).all()

    def test_rolling_nan(self, analyzed_data):
        assert pd.isna(
            analyzed_data.loc[0, ["rolling_volatility", "moving_average"]]
        ).all()
        assert pd.isna(analyzed_data.loc[1, "rolling_volatility"])


class TestNumericReturn:

    def test_returns(self, analyzed_data):
        expected_daily_return_value = (
            analyzed_data.loc[2, "close"] / analyzed_data.loc[1, "close"] - 1
        )
        expected_log_return_value = np.log(
            analyzed_data.loc[2, "close"] / analyzed_data.loc[1, "close"]
        )
        assert np.isclose(
            analyzed_data.loc[2, "daily_return"], expected_daily_return_value, atol=1e-8
        )

        assert np.isclose(
            analyzed_data.loc[2, "log_return"], expected_log_return_value, atol=1e-8
        )

    def test_rolling_window(self, analyzed_data):
        expected_rolling_volatility_value = (
            analyzed_data["log_return"].rolling(window=2).std()
        )
        expected_moving_average_value = analyzed_data["close"].rolling(window=2).mean()
        assert np.isclose(
            analyzed_data.loc[2, "rolling_volatility"],
            expected_rolling_volatility_value[2],
            atol=1e-8,
        )
        assert np.isclose(
            analyzed_data.loc[2, "moving_average"],
            expected_moving_average_value[2],
            atol=1e-8,
        )


class TestRangeFeature:

    @pytest.mark.parametrize(
        "feature,expected_formula,rows",
        [
            ("absolute_range", lambda df: df["high"] - df["low"], [0, 1, 2]),
            (
                "relative_range_on_open",
                lambda df: (df["high"] - df["low"]) / df["open"],
                [0, 1, 2],
            ),
            (
                "relative_range_on_close",
                lambda df: (df["high"] - df["low"]) / df["close"],
                [0, 1, 2],
            ),
            ("open_close_range", lambda df: df["close"] - df["open"], [0, 1, 2]),
            (
                "upper_shadow",
                lambda df: df["high"] - df[["open", "close"]].max(axis=1),
                [0, 1, 2],
            ),
            (
                "lower_shadow",
                lambda df: df[["open", "close"]].min(axis=1) - df["low"],
                [0, 1, 2],
            ),
        ],
    )
    def test_range_calculation(self, analyzed_data, feature, expected_formula, rows):

        expected = expected_formula(analyzed_data)
        print(f"\n{feature}: {expected}")

        assert np.isclose(analyzed_data.loc[rows, feature], expected, atol=1e-8).all()
