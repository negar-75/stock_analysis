"""
Feature engineering module for stock price data.

Calculates technical indicators and derived metrics.
"""

import numpy as np


class FeatureEngineering:
    def __init__(self, data, volatility_window, moving_window):
        self.data = data
        self._shifted_close = self.data["close"].shift(1)
        self._volatility_window = volatility_window
        self._moving_window = moving_window

    def daily_return(self):
        self.data["daily_return"] = self.data["close"] / self._shifted_close - 1
        return self

    def log_return(self):
        self.data["log_return"] = np.log(self.data["close"] / self._shifted_close)
        return self

    def rolling_volatility(self):
        self.data["rolling_volatility"] = (
            self.data["log_return"].rolling(window=self._volatility_window).std()
        )
        return self

    def moving_average(self):
        self.data["moving_average"] = (
            self.data["close"].rolling(window=self._moving_window).mean()
        )
        return self

    def absolute_range(self):
        self.data["absolute_range"] = self.data["high"] - self.data["low"]
        return self

    def relative_range_on_open(self):
        if "absolute_range" not in self.data:
            self.absolute_range()
        self.data["relative_range_on_open"] = (self.data["absolute_range"]) / self.data[
            "open"
        ]
        return self

    def relative_range_on_close(self):
        self.data["relative_range_on_close"] = (
            self.data["high"] - self.data["low"]
        ) / self.data["close"]
        return self

    def close_open_range(self):
        self.data["open_close_range"] = self.data["close"] - self.data["open"]
        return self

    def upper_wick(self):
        self.data["upper_shadow"] = self.data["high"] - self.data[
            ["open", "close"]
        ].max(axis=1)
        return self

    def lower_wick(self):
        self.data["lower_shadow"] = (
            self.data[["open", "close"]].min(axis=1) - self.data["low"]
        )
        return self

    def run(self):
        feature_methods = [
            self.daily_return,
            self.log_return,
            self.rolling_volatility,
            self.moving_average,
            self.absolute_range,
            self.relative_range_on_open,
            self.relative_range_on_close,
            self.close_open_range,
            self.upper_wick,
            self.lower_wick,
        ]

        for method in feature_methods:
            method()

        return self.data
