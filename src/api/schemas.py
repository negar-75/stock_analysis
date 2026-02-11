from pydantic import BaseModel, ConfigDict, Field, field_validator
import math
from datetime import date
from decimal import Decimal


class DailyPriceResponse(BaseModel):

    date: date
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: int

    daily_return: float | None = None
    log_return: float | None = None
    rolling_volatility: float | None = None
    moving_average: float | None = None

    absolute_range: float
    relative_range_on_open: float
    relative_range_on_close: float
    open_close_range: float
    upper_shadow: float
    lower_shadow: float

    @field_validator("*", mode="before")
    @classmethod
    def clean_nan(cls, v):
        # Handle Decimal NaN
        if isinstance(v, Decimal):
            if v.is_nan() or v.is_infinite():
                return None
            return float(v)
        # Handle float NaN
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v


class PaginationMeta(BaseModel):
    total_records: int
    current_page: int
    total_pages: int


class PaginatedDailyPrices(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: list[DailyPriceResponse]
    pagination: PaginationMeta


class DailyPriceInput(BaseModel):
    ticker: str
    start_date: date
    end_date: date
    limit: int = Field(gt=0, le=100)
    offset: int = Field(ge=0)

    @field_validator("*", mode="before")
    @classmethod
    def clean_nan(cls, v):
        # Handle Decimal NaN
        if isinstance(v, Decimal):
            if v.is_nan() or v.is_infinite():
                return None
            return float(v)
        # Handle float NaN
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v
