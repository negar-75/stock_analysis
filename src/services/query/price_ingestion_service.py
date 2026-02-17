import logging
from datetime import date
from typing import List, Tuple
from sqlalchemy.orm import Session
from src.core.exceptions import MarketAPIError, NoDataAvailableError
from src.pipelines.orchestrators.stock_pipeline import StockDataPipeline
from src.core.pipeline_config import DTYPES
from src.repositories.price_repository import PriceRepository
from src.pipelines.ingestions.market_api import Ingestion


logger = logging.getLogger(__name__)


class PriceIngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PriceRepository(db)

    def ingest_and_store_price(
        self,
        ticker: str,
        ranges: List[[Tuple[date, date]]],
        volatility_window: int = 15,
        moving_window: int = 15,
    ):
        logger.info("Ingestion started | ticker=%s | ranges=%s", ticker, ranges)
        total_fetched = 0
        total_inserted = 0
        failed_ranges = []
        for start_range, end_range in ranges:
            try:
                logger.info(
                    "Fetching market data | ticker=%s | %s → %s",
                    ticker,
                    start_range,
                    end_range,
                )

                raw_df = Ingestion(str(start_range), str(end_range), ticker).run()
                fetched = len(raw_df)
                if raw_df.empty:
                    raise NoDataAvailableError(
                        f"No data available for '{ticker}' between {start_range} and {end_range}. "
                        f"Please check: ticker symbol is correct, date range is valid, and dates are trading days."
                    )
                total_fetched += fetched

                logger.info(
                    "Fetched rows=%s | ticker=%s | %s → %s",
                    fetched,
                    ticker,
                    start_range,
                    end_range,
                )

                processed_df = StockDataPipeline(
                    DTYPES, raw_df, volatility_window, moving_window
                ).run()

                inserted = self.repository.bulk_insert(processed_df)
                total_inserted += inserted

                logger.info(
                    "Inserted rows=%s | ticker=%s | %s → %s",
                    inserted,
                    ticker,
                    start_range,
                    end_range,
                )

            except NoDataAvailableError:
                logger.info(
                    "No data | ticker=%s | %s → %s", ticker, start_range, end_range
                )
                continue

            except MarketAPIError as e:
                logger.error(
                    "Market API error | ticker=%s | %s → %s | error=%s",
                    ticker,
                    start_range,
                    end_range,
                    e,
                )
                failed_ranges.append((start_range, end_range, str(e)))

        self.db.commit()
        message = (
            "Completed with errors"
            if failed_ranges
            else (
                "No new data"
                if total_inserted == 0
                else f"Inserted {total_inserted} rows"
            )
        )

        logger.info(
            "Ingestion finished | ticker=%s | fetched=%s | inserted=%s | status=%s",
            ticker,
            total_fetched,
            total_inserted,
            message,
        )

        result = {
            "ticker": ticker,
            "total_fetched": total_fetched,
            "total_inserted": total_inserted,
            "message": message,
        }

        if failed_ranges:
            result["errors"] = failed_ranges

        return result
