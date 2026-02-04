import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from src.db.models import DailyPrices

from sqlalchemy.orm import Session


def write_data_to_db(data: pd.DataFrame, engine):
    records = data.to_dict(orient="records")

    stmt = insert(DailyPrices).values(records)
    stmt = stmt.on_conflict_do_nothing(index_elements=["date"])

    with engine.begin() as conn:
        result = conn.execute(stmt)
    return result.rowcount


def read_db_by_col(db: Session) -> pd.DataFrame:
    query = db.query(DailyPrices.date, DailyPrices.close).order_by(DailyPrices.date)
    return pd.read_sql(query.statement, db.bind)
