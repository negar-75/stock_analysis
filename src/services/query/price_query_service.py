from sqlalchemy.orm import Session
from math import ceil
import logging
from src.repositories.price_repository import PriceRepository
from src.services.query.price_ingestion_service import PriceIngestionService
from src.api.schemas import DailyPriceQueryInput, PaginatedDailyPrices


logger = logging.getLogger(__name__)


class PriceQueryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PriceRepository(self.db)
        self.ingestion_service = PriceIngestionService(self.db)

    def get_price(self, params: DailyPriceQueryInput) -> PaginatedDailyPrices:
        logger.info(
            "Query started | ticker=%s | %s → %s | limit=%s | offset=%s",
            params.ticker,
            params.start_date,
            params.end_date,
            params.limit,
            params.offset,
        )
        missing_range = self.repository.get_missing_data_range(
            params.ticker, params.start_date, params.end_date
        )
        ingestion_result = None
        if missing_range:
            logger.info(
                "Missing data detected | ticker=%s | ranges=%s",
                params.ticker,
                missing_range,
            )

            ingestion_result = self.ingestion_service.ingest_and_store_price(
                params.ticker, missing_range
            )

            logger.info(
                "Ingestion summary | ticker=%s | fetched=%s | inserted=%s",
                params.ticker,
                ingestion_result["total_fetched"],
                ingestion_result["total_inserted"],
            )
        total = self.repository.count_prices(
            params.ticker, params.start_date, params.end_date
        )
        rows = self.repository.fetch_prices(
            params.ticker,
            params.start_date,
            params.end_date,
            params.limit,
            params.offset,
        )
        print(rows)
        logger.info(
            "DB query complete | ticker=%s | total=%s | returned=%s",
            params.ticker,
            total,
            len(rows),
        )
        current_page = (params.offset // params.limit) + 1 if total > 0 else 0
        total_pages = ceil(total / params.limit) if total > 0 else 0

        logger.info(
            "Query finished | ticker=%s | page=%s/%s",
            params.ticker,
            current_page,
            total_pages,
        )
        return {
            "data": rows,
            "pagination": {
                "total_records": total,
                "current_page": current_page,
                "total_pages": total_pages,
            },
        }
