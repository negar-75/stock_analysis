import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from src.db.models import DailyPrices
from src.db.connection import get_engine, SessionLocal
from sqlalchemy.orm import Session


engine = get_engine()


def write_csv_to_db(data: pd.DataFrame):
    records = data.to_dict(orient="records")

    stmt = insert(DailyPrices).values(records)
    stmt = stmt.on_conflict_do_nothing(index_elements=["date"])

    with engine.begin() as conn:
        conn.execute(stmt)


def read_db_by_col(db: Session) -> pd.DataFrame:
    query = db.query(DailyPrices.date, DailyPrices.close).order_by(DailyPrices.date)
    return pd.read_sql(query.statement, db.bind)
