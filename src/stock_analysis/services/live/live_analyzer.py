import logging
from stock_analysis.api.schemas.price import DailyPriceLiveInput, DailyPriceLiveResponse
from stock_analysis.core.pipeline_config import DTYPES
from stock_analysis.core.exceptions import MarketAPIError, NoDataAvailableError
from stock_analysis.pipelines.ingestions.market_api import Ingestion
from stock_analysis.pipelines.orchestrators.stock_pipeline import StockDataPipeline

logger = logging.getLogger(__name__)


class OnDemandAnalysisService:
    def get_price(self, params: DailyPriceLiveInput) -> DailyPriceLiveResponse:
        logger.info(
            "Query started | ticker=%s | %s → %s ",
            params.ticker,
            params.start_date,
            params.end_date,
        )

        try:
            logger.info(
                "Fetching market data | ticker=%s | %s → %s",
                params.ticker,
                params.start_date,
                params.end_date,
            )

            raw_df = Ingestion(
                str(params.start_date), str(params.end_date), params.ticker
            ).run()

            # Check if dataframe is empty
            if raw_df is None or raw_df.empty:
                raise NoDataAvailableError(
                    f"No data available for '{params.ticker}' between {params.start_date} and {params.end_date}. "
                    f"Please check: ticker symbol is correct, date range is valid, and dates are trading days."
                )

            fetched = len(raw_df)

            logger.info(
                "Fetched rows=%s | ticker=%s | %s → %s",
                fetched,
                params.ticker,
                params.start_date,
                params.end_date,
            )

            processed_df = StockDataPipeline(
                DTYPES, raw_df, params.volatility_window, params.moving_window
            ).run()

            data = processed_df.to_dict(orient="records")
            return DailyPriceLiveResponse(
                data=data, total_records=fetched, error_message=None, error_type=None
            )

        except NoDataAvailableError as e:

            logger.warning(
                "No data | ticker=%s | %s → %s | error=%s",
                params.ticker,
                params.start_date,
                params.end_date,
                str(e),
            )
            return DailyPriceLiveResponse(
                data=[],
                total_records=0,
                error_message=str(e),
                error_type="NO_DATA_AVAILABLE",
            )

        except MarketAPIError as e:
            logger.error(
                "Market API error | ticker=%s | %s → %s | error=%s",
                params.ticker,
                params.start_date,
                params.end_date,
                str(e),
            )
            return DailyPriceLiveResponse(
                data=[], total_records=0, error_message=str(e), error_type="API_ERROR"
            )
        except Exception as e:
            # Catch-all for unexpected errors
            logger.exception(
                "Unexpected error | ticker=%s | %s → %s",
                params.ticker,
                params.start_date,
                params.end_date,
            )
            return DailyPriceLiveResponse(
                data=[],
                total_records=0,
                error_message=f"Unexpected error: {str(e)}",
                error_type="INTERNAL_ERROR",
            )
