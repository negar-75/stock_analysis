"""
Pipeline configuration for stock data.

Defines expected column names and dtypes for raw market data
before validation and feature engineering.
"""

DTYPES = {
    "Date": "datetime64[ns, America/New_York]",
    "Ticker": "object",
    "Open": "float64",
    "High": "float64",
    "Low": "float64",
    "Close": "float64",
    "Volume": "int64",
}
