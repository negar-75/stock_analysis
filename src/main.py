from src.ingestions.market_api import Ingestion
from src.pipeline import run_pipeline
from src.db.connection import get_engine


START_DATE = "2025-01-01"
END_DATE = "2026-01-01"
STOCK = "MSFT"

DTYPES = {
    "Date": "datetime64[ns, America/New_York]",
    "Open": "float64",
    "High": "float64",
    "Low": "float64",
    "Close": "float64",
    "Volume": "int64",
}

if __name__ == "__main__":
    engine = get_engine("DB_NAME")
    try:
        raw_data = Ingestion(START_DATE, END_DATE, STOCK)
        inserted_rows_to_db = run_pipeline(DTYPES, raw_data.run(), engine)
        print(f"{inserted_rows_to_db} rows has been inserted into daily price table")
    finally:
        engine.dispose()
