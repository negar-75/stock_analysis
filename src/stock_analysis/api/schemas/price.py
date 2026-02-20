from pydantic import BaseModel, ConfigDict, Field, field_validator
import math
from datetime import date
from decimal import Decimal
import re
from typing import Optional, ClassVar, Set


class TickerValidationMixin(BaseModel):
    """Mixin for ticker validation"""

    ticker: str

    # Regex pattern for valid ticker symbols
    TICKER_PATTERN: ClassVar[re.Pattern] = re.compile(r"^[A-Z]{1,5}(-[A-Z])?$")
    INVALID_VALUES: ClassVar[Set[str]] = {"NONE", "NULL", "UNDEFINED", "NA", "N/A", ""}

    @field_validator("ticker")
    @classmethod
    def validate_ticker_format(cls, v: str) -> str:
        """Validate ticker format and basic rules"""
        if not v or not isinstance(v, str):
            raise ValueError("Ticker is required and must be a string")

        # Clean and normalize
        ticker = v.strip().upper()

        # Check for invalid values
        if ticker in cls.INVALID_VALUES:
            raise ValueError(f"Invalid ticker value: '{v}'")

        # Check format
        if not cls.TICKER_PATTERN.match(ticker):
            raise ValueError(
                f"Invalid ticker format: '{v}'. "
                "Ticker must be 1-5 uppercase letters (e.g., AAPL, MSFT, BRK-A)"
            )

        return ticker


class DateRangeValidator(BaseModel):
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def validate_date_range(cls, end_date: date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must be >= start_date")
        return end_date


class CleanNaNModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def clean_nan(cls, v):
        if isinstance(v, Decimal):
            if v.is_nan() or v.is_infinite():
                return None
            return float(v)
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v


class DailyPriceResponse(CleanNaNModel):
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


class PaginationMeta(BaseModel):
    total_records: int
    current_page: int
    total_pages: int


class PaginatedDailyPrices(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: list[DailyPriceResponse]
    pagination: PaginationMeta


class DailyPriceQueryInput(DateRangeValidator, TickerValidationMixin):

    limit: int = Field(gt=0, le=100)
    offset: int = Field(ge=0)


class DailyPriceLiveInput(DateRangeValidator, TickerValidationMixin):

    volatility_window: int = 15
    moving_window: int = 10


class DailyPriceLiveResponse(BaseModel):
    data: list[DailyPriceResponse]
    total_records: int
    error_message: Optional[str] = None
    error_type: Optional[str] = None
