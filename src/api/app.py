from fastapi import FastAPI, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session
from src.api.dependencies.db import get_db
from src.api.schemas import PaginatedDailyPrices, DailyPriceInput
from src.core.logging_config import setup_logging
from src.services.price_query_service import PriceQueryService


def get_session():
    yield from get_db()


setup_logging()
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my first API application"}


@app.get("/prices", response_model=PaginatedDailyPrices)
def get_prices(
    params: Annotated[DailyPriceInput, Query()],
    db: Session = Depends(get_session),
) -> PaginatedDailyPrices:
    return PriceQueryService(db).get_price(params)
