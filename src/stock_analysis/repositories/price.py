"""
Repository for price data access.

Handles all database queries related to price data.
"""

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from datetime import date, timedelta
from typing import List, Tuple, Optional
from stock_analysis.db.models.daily_prices import DailyPrices


class PriceRepository:
    """Repository for querying and inserting daily price data."""

    def __init__(self, db: Session):
        self.db = db

    def fetch_prices(
        self, ticker: str, start_date: date, end_date: date, limit: int, offset: int
    ):
        """Fetch paginated daily prices for a ticker within a date range."""
        return (
            self.db.query(DailyPrices)
            .filter(
                DailyPrices.date >= start_date,
                DailyPrices.date <= end_date,
                DailyPrices.ticker == ticker,
            )
            .order_by(DailyPrices.date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def count_prices(
        self,
        ticker: str,
        start_date: date,
        end_date: date,
    ) -> int:
        """Count total daily prices for a ticker within a date range."""
        return (
            self.db.query(func.count(DailyPrices.id))
            .filter(
                DailyPrices.date >= start_date,
                DailyPrices.date <= end_date,
                DailyPrices.ticker == ticker,
            )
            .scalar()
        )

    def bulk_insert(self, data: pd.DataFrame) -> int:
        """Insert price records in bulk, skipping conflicts on ticker+date."""
        records = data.to_dict(orient="records")

        stmt = insert(DailyPrices).values(records)
        stmt = stmt.on_conflict_do_nothing(index_elements=["ticker", "date"])

        result = self.db.execute(stmt)

        return result.rowcount

    def get_min_max_date(self, ticker: str) -> Tuple[Optional[date], Optional[date]]:
        """Get the earliest and latest date for a ticker in the database."""
        result = (
            self.db.query(func.min(DailyPrices.date), func.max(DailyPrices.date))
            .filter(DailyPrices.ticker == ticker)
            .one()
        )
        return result

    def get_missing_data_range(
        self, ticker: str, start_date: date, end_date: date
    ) -> List[Tuple[date, date]]:
        """Return date ranges that are missing from the database for the given ticker."""
        min_date, max_date = self.get_min_max_date(ticker)
        if min_date is None or max_date is None:
            return [(start_date, end_date)]
        if end_date < min_date or start_date > max_date:
            return [(start_date, end_date)]
        missing = []
        if start_date < min_date:
            missing.append((start_date, min_date - timedelta(days=1)))
        if end_date > max_date:
            missing.append((max_date + timedelta(days=1), end_date))
        return missing
