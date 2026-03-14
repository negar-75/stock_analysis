"""
Price API router.

Provides on-demand stock price analysis endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Query

from stock_analysis.schemas.price import DailyPriceLiveInput, DailyPriceLiveResponse
from stock_analysis.services.price.historical_service import OnDemandAnalysisService


router = APIRouter()


@router.get("/historical", response_model=DailyPriceLiveResponse)
async def get_historical_prices(
    params: Annotated[DailyPriceLiveInput, Query()],
) -> DailyPriceLiveResponse:
    """
    Get stock prices for the given ticker and date range.

    Returns live analysis with technical indicators (returns, volatility, etc.).
    """
    return await OnDemandAnalysisService().get_price(params)
