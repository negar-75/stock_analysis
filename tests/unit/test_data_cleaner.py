import pandas as pd
import pytest
from src.pipelines.transformers.data_cleaner import (
    convert_to_datetime,
    sort_by_column,
    drop_duplicates,
    col_name_normalization,
    col_ordering,
    clean_data,
)


def test_convert_to_datetime_right_input():
    """
    Verify convert_to_datetime returns True for valid date strings
    and converts the column to datetime successfully.
    """
    data = pd.DataFrame({"Date": ["2020-01-01", "2020-12-31"]})
    result = convert_to_datetime(data, "Date")

    assert result is True


def test_convert_to_datetime_wrong_input():
    """
    Verify convert_to_datetime returns False when date strings
    cannot be parsed into datetime format.
    """
    data = pd.DataFrame({"Date": ["abc", "2020-12-3"]})

    result = convert_to_datetime(data, "Date")
    assert result is False


def test_sort_by_column_right_input():
    data = pd.DataFrame(
        {"date": ["2020-01-03", "2020-01-01", "2020-01-02"], "open": [10, 12, 11]}
    )
    result = sort_by_column(data, "date")
    expected_dates = ["2020-01-01", "2020-01-02", "2020-01-03"]
    assert result["date"].tolist() == expected_dates


def test_sort_by_column_wrong_input():
    data = pd.DataFrame({"open": [10, 12, 11]})
    with pytest.raises(KeyError):
        sort_by_column(data, "date")


def test_drop_duplicates_right_input():
    data = pd.DataFrame(
        {"date": ["2020-01-01", "2020-01-01", "2020-01-02"], "open": [10, 10, 12]}
    )

    result = drop_duplicates(data, "date")
    assert len(result) == 2
    assert result["date"].to_list() == ["2020-01-01", "2020-01-02"]


def test_drop_duplicates_wrong_input():
    data = pd.DataFrame({"open": [10, 10, 12]})

    with pytest.raises(KeyError):
        drop_duplicates(data, "date")


def test_col_name_normalization_right_input():
    data = pd.DataFrame({"Date": ["2020-01-03", "2020-01-01", "2020-01-02"]})
    result = col_name_normalization(data)
    assert result == ["date"]


def test_col_name_normalization_wrong_input():
    data = pd.DataFrame({})
    result = col_name_normalization(data)
    assert result == []


def test_col_ordering_right_input():
    data = pd.DataFrame(
        {
            "date": ["2020-01-01", "2020-01-01", "2020-01-02"],
            "open": [10, 10, 12],
            "close": [12, 10, 9.6],
        }
    )
    order = ["date", "close", "open"]
    result = col_ordering(data, order)
    assert list(result.keys()) == order


def test_col_ordering_wrong_input():
    data = pd.DataFrame(
        {
            "date": ["2020-01-01", "2020-01-01", "2020-01-02"],
            "open": [10, 10, 12],
            "close": [12, 10, 9.6],
        }
    )
    order = ["date", "close", "open", "high"]
    with pytest.raises(KeyError):
        col_ordering(data, order)


def test_clean_data_right_input():
    data = pd.DataFrame(
        {
            "Date": ["2020-01-02", "2020-01-01", "2020-01-02"],
            "Open": [12, 10, 12],
            "High": [15, 14, 15],
            "Low": [9, 8, 9],
            "Close": [13, 11, 13],
            "Volume": [1000, 1500, 1000],
            "Extra": ["x", "y", "z"],  # extra column that should be removed
        }
    )
    result = clean_data(data)
    assert list(result.columns) == [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    assert len(result) == 2
    print(result["date"].tolist())
    assert result["date"].tolist() == list(
        pd.to_datetime(["2020-01-01", "2020-01-02"]).date
    )  #
