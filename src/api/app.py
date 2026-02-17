from fastapi import FastAPI, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session
from src.api.dependencies.db import get_db
from src.api.schemas import (
    PaginatedDailyPrices,
    DailyPriceQueryInput,
    DailyPriceLiveInput,
    DailyPriceLiveResponse,
)
from src.core.logging_config import setup_logging
from src.services.query.price_query_service import PriceQueryService
from src.services.live.live_analyzer import OnDemandAnalysisService


def get_session():
    yield from get_db()


setup_logging()
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my first API application"}


@app.get("/prices", response_model=DailyPriceLiveResponse)
def get_prices(
    params: Annotated[DailyPriceLiveInput, Query()],
    db: Session = Depends(get_session),
) -> DailyPriceLiveResponse:
    return OnDemandAnalysisService().get_price(params)
    # return PriceQueryService(db).get_price(params)
