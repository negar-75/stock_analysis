from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session
from src.api.dependencies.db import get_session
from src.api.schemas.price import (
    # PaginatedDailyPrices,
    # DailyPriceQueryInput,
    DailyPriceLiveInput,
    DailyPriceLiveResponse,
)

# from src.services.query.price_query_service import PriceQueryService
from src.services.live.live_analyzer import OnDemandAnalysisService


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to my first API application"}


@router.get("/prices", response_model=DailyPriceLiveResponse)
def get_prices(
    params: Annotated[
        DailyPriceLiveInput, Query()
    ],  # UQuery Params With pydantic Model
    db: Session = Depends(get_session),
) -> DailyPriceLiveResponse:
    return OnDemandAnalysisService().get_price(params)
    # return PriceQueryService(db).get_price(params)
