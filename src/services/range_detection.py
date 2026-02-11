from sqlalchemy.orm import Session
from src.db.models.daily_prices import DailyPrices
from sqlalchemy import func
from datetime import date


def get_missing_date_ranges(
    ticker: str, start_date: date, end_date: date, db_session: Session
):

    min_date, max_date = (
        db_session.query(func.min(DailyPrices.date), func.max(DailyPrices.date))
        .filter(DailyPrices.ticker == ticker)
        .one()
    )
    if min_date is None or max_date is None:
        return [(start_date, end_date)]
    if end_date < min_date or start_date > max_date:
        return [(start_date, end_date)]
    missing = []

    if start_date < min_date:
        missing.append((start_date, min_date))
    if end_date > max_date:
        missing.append((max_date, end_date))

    return missing
