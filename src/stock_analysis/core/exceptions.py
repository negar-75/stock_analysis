"""
Custom exceptions for the stock analysis application.

Includes ingestion errors and user-related errors.
"""


# ---------- Ingestion Exceptions ----------
class IngestionError(Exception):
    """Base exception for ingestion errors."""

    pass


class NoDataAvailableError(IngestionError):
    """Raised when no market data exists for requested range."""

    pass


class MarketAPIError(IngestionError):
    """Raised when external market API fails."""

    pass


# ---------- User Exceptions ----------


class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user that already exists."""

    pass


class InvalidCredentialError(Exception):
    """Raised when authentication credentials are invalid."""

    pass


class UserNotFound(Exception):
    """Raised when a requested user does not exist."""

    pass
