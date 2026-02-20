# ----------Ingestion_Exceptions#----------
class IngestionError(Exception):
    """Base exception for ingestion errors."""

    pass


class NoDataAvailableError(IngestionError):
    """Raised when no market data exists for requested range."""

    pass


class MarketAPIError(IngestionError):
    """Raised when external market API fails."""

    pass
