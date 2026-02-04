from fastapi import FastAPI, Depends, HTTPException
from datetime import date
from math import ceil
from sqlalchemy.orm import Session
from typing import List, Optional
from src.db.connection import get_db, get_engine
from src.db.models import DailyPrices
from src.api.schemas import PaginatedDailyPrices


engine = get_engine("DB_NAME")


def get_session():
    yield from get_db(engine)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my first API application"}


@app.get("/prices", response_model=PaginatedDailyPrices)
def get_prices(
    limit: int = 10,
    offset: int = 0,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_session),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be <= end_date")
    if limit <= 0 or limit >= 100:
        raise HTTPException(status_code=400, detail="limit must be between 0 and 100")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset should be more than 0")
    query = db.query(DailyPrices)
    total_records = query.count()
    current_page = (offset // limit) + 1 if total_records > 0 else 0
    total_pages = ceil(total_records / limit) if total_records > 0 else 0
    if start_date:
        query = query.filter(DailyPrices.date >= start_date)
    if end_date:
        query = query.filter(DailyPrices.date <= end_date)
    result = query.order_by(DailyPrices.date.desc()).offset(offset).limit(limit).all()

    return {
        "data": result,
        "pagination": {
            "total_records": total_records,
            "current_page": current_page,
            "total_pages": total_pages,
        },
    }
