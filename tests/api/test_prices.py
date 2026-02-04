from fastapi.testclient import TestClient
from src.api.app import app
from math import ceil
import pytest

BASE_URL = "/prices"
client = TestClient(app)


def test_successful_response_structure():
    response = client.get(BASE_URL)
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "pagination" in json_data
    pagination = json_data["pagination"]
    assert "total_pages" in pagination
    assert "total_records" in pagination
    assert "current_page" in pagination


def test_date_range_filtering():
    start_date = "2025-10-01"
    end_date = "2025-10-10"
    response = client.get(f"{BASE_URL}?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    data = response.json()["data"]
    for record in data:
        record_date = record["date"]
        assert (
            start_date <= record_date <= end_date
        ), f"Record date {record_date} outside range [{start_date}, {end_date}]"


def test_pagination_limit_and_offset():
    limit = 10
    offset = 0
    response = client.get(f"{BASE_URL}?limit={limit}&offset={offset}")
    assert response.status_code == 200
    json_data = response.json()
    data = json_data["data"]
    assert len(data) <= limit, f"Expected {limit} records, got {len(data)}"
    pagination = json_data["pagination"]
    expected_total_pages = ceil(pagination["total_records"] / limit)
    assert (
        expected_total_pages == pagination["total_pages"]
    ), f"Expected {expected_total_pages} total pages, got {pagination['total_pages']}"


@pytest.mark.parametrize(
    "limit,offset,expected_page",
    [
        (10, 0, 1),
        (10, 10, 2),
        (20, 0, 1),
        (
            5,
            15,
            4,
        ),
    ],
)
def test_pagination_various_limits(limit, offset, expected_page):
    response = client.get(f"{BASE_URL}?limit={limit}&offset={offset}")
    assert response.status_code == 200
    pagination = response.json()["pagination"]
    assert expected_page == pagination["current_page"]


def test_empty_date_range_returns_empty_data():
    start_date = "2099-10-01"
    end_date = "2099-10-10"
    response = client.get(f"{BASE_URL}?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_invalid_date_format_returns_error():
    start_date = "invalid"
    end_date = "invalid"
    response = client.get(f"{BASE_URL}?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 422
