from stock_analysis.schemas.price import DailyPriceLiveInput


def build_stock_cache_key(params: DailyPriceLiveInput):
    return (
        f"stock:{params.ticker}:"
        f"{params.start_date}:"
        f"{params.end_date}:"
        f"{params.volatility_window}:"
        f"{params.moving_window}:"
    )
