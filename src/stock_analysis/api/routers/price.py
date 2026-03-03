from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session
from stock_analysis.api.dependencies.db import get_db
from stock_analysis.api.schemas.price import (
    # PaginatedDailyPrices,
    # DailyPriceQueryInput,
    DailyPriceLiveInput,
    DailyPriceLiveResponse,
)

# from stock_analysis.services.query.price_query_service import PriceQueryService
from stock_analysis.services.live.live_analyzer import OnDemandAnalysisService


router = APIRouter()


@router.get("/", response_model=DailyPriceLiveResponse)
def get_prices(
    params: Annotated[
        DailyPriceLiveInput, Query()
    ],  # UQuery Params With pydantic Model
    db: Session = Depends(get_db),
) -> DailyPriceLiveResponse:
    return OnDemandAnalysisService().get_price(params)
    # return PriceQueryService(db).get_price(params)
