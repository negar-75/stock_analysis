import logging
from typing import Optional
import pandas as pd
import yfinance as yf
from src.core.exceptions import MarketAPIError, NoDataAvailableError


logger = logging.getLogger(__name__)


class Ingestion:
    def __init__(self, start_date: str, end_date: str, ticker: str):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.data: Optional[pd.DataFrame] = None

    # Fetch from API
    def fetch(self):
        logger.info(
            "Fetching %s data from %s to %s",
            self.ticker,
            self.start_date,
            self.end_date,
        )

        try:
            ticker_client = yf.Ticker(self.ticker)

            self.data = ticker_client.history(
                start=self.start_date,
                end=self.end_date,
                interval="1d",
            )

        # External / infrastructure failure → wrap
        except Exception as e:
            logger.exception(
                "Market API failure  for %s from %s → %s",
                self.ticker,
                self.start_date,
                self.end_date,
            )
            raise MarketAPIError(f"Failed to fetch data for {self.ticker}") from e
        if self.data is None or self.data.empty:
            raise NoDataAvailableError(
                f"No data for {self.ticker} "
                f"from {self.start_date} to {self.end_date}"
            )

        logger.info("Fetched %s records for %s", len(self.data), self.ticker)

        return self

    # Cleaning helpers
    def drop_extra_columns(self):
        if self.data is None:
            return self

        columns_to_drop = ["Dividends", "Stock Splits"]
        existing = [c for c in columns_to_drop if c in self.data.columns]

        if existing:
            self.data = self.data.drop(existing, axis=1)
            logger.debug("Dropped columns: %s", existing)

        return self

    def convert_index_to_col(self):
        if self.data is not None:
            self.data["Date"] = self.data.index
        return self

    def remove_index(self):
        if self.data is not None:
            self.data.reset_index(drop=True, inplace=True)
        return self

    def add_ticker_column(self):
        if self.data is not None:
            self.data["Ticker"] = self.ticker
        return self

    # Public entry
    def run(self) -> pd.DataFrame:
        """
        Execute full ingestion pipeline.

        Returns:
            Cleaned DataFrame with market data.

        Raises:
            NoDataAvailableError
            MarketAPIError
        """
        (
            self.fetch()
            .drop_extra_columns()
            .convert_index_to_col()
            .remove_index()
            .add_ticker_column()
        )

        logger.info(
            "Ingestion complete: %s records for %s", len(self.data), self.ticker
        )

        return self.data
