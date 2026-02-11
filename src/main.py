from datetime import date
from src.services.price_ingestion_service import PriceIngestionService
from src.db.session import SessionLocal
from src.core.logging_config import setup_logging


START_DATE = "2024-11-25"
END_DATE = "2026-01-31"
TICKER = "MSFT"
setup_logging()
if __name__ == "__main__":
    with SessionLocal() as db:
        ingested_data = PriceIngestionService(db)
        data_fetched = ingested_data.ingest_and_store_price(
            TICKER, date.fromisoformat(START_DATE), date.fromisoformat(END_DATE), 15, 5
        )
