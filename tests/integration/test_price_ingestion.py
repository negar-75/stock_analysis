from unittest.mock import patch
from src.services.query.price_ingestion_service import PriceIngestionService
from datetime import date
import pandas as pd
from src.core.exceptions import MarketAPIError




@patch("src.services.query.price_ingestion_service.Ingestion.run")
def test_ingestion_success(mock_run,test_setup_session,get_mock_price_data):
    mock_run.return_value = get_mock_price_data()
    service = PriceIngestionService(test_setup_session)
    result = service.ingest_and_store_price(ticker="AAPL",
        ranges=[(date(2025, 1, 1), date(2025, 1, 10))],
        volatility_window=3,
        moving_window=3,)
    assert result["ticker"] == "AAPL"
    assert result["total_fetched"] == 10
    assert result["total_inserted"] == 10
    assert result["message"].startswith("Inserted")
    

@patch("src.services.query.price_ingestion_service.Ingestion.run")
def test_ingestion_no_data(mock_run,test_setup_session):

    mock_run.return_value = pd.DataFrame()
    service = PriceIngestionService(test_setup_session)
    result = service.ingest_and_store_price(ticker="AAPL",
        ranges=[(date(2025, 1, 1), date(2025, 1, 10))],
        volatility_window=3,
        moving_window=3,)
    
    assert result["total_fetched"] == 0
    assert result["total_inserted"] == 0
    assert result["message"].startswith("No new data")
    

@patch("src.services.query.price_ingestion_service.Ingestion.run")
def test_ingestion_failure(mock_run,test_setup_session,get_mock_price_data):

    mock_run.side_effect = [
        get_mock_price_data(),
        MarketAPIError("API down")
    ]

    service = PriceIngestionService(test_setup_session)
    result = service.ingest_and_store_price(ticker="AAPL",
        ranges=[(date(2025, 1, 1), date(2025, 1, 10)),(date(2025, 1, 15), date(2025, 1, 20))],
        volatility_window=3,
        moving_window=3,)
    print(result)
    assert result["ticker"] == "AAPL"
    assert result["total_fetched"] == 10
    assert result["total_inserted"] == 10
    assert result["message"].startswith("Completed with errors")
    assert len(result["errors"]) == 1


