from pydantic import BaseModel, ConfigDict
from datetime import date


class DailyPriceResponse(BaseModel):

    date: date
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
