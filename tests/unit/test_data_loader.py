from src.pipelines.validators.data_validator import (
    required_columns_exist,
    check_column_type,
    check_corrupted_values,
    check_logical_consistency,
)
import pandas as pd


def test_required_columns_exist_right_input():
    """
    Verify required_columns_exist returns True when all required
    columns are present in the DataFrame.
    """
    data = pd.DataFrame(
        {
            "Date": ["2020-01-01"],
            "Open": [12],
            "High": [15],
            "Low": [11.9],
            "Close": [13],
            "Volume": [200],
        }
    )
    col_list = ["Date", "High", "Low", "Close", "Volume", "Open"]

    result = required_columns_exist(data, col_list)

    assert result is True


def test_required_columns_exist_wrong_input():
    """
    Verify required_columns_exist returns False when one or more
    required columns are missing.
    """
    data = pd.DataFrame(
        {
            "Date": ["2020-01-01"],
            "Open": [12],
            "High": [15],
            "Low": [11.9],
            "Close": [13],
        }
    )
    col_list = ["Date", "High", "Low", "Close", "Volume"]

    result = required_columns_exist(data, col_list)

    assert result is False


def test_check_column_type_right_input():
    """
    Verify check_column_type returns True when all columns match
    their expected data types.
    """
    data = pd.DataFrame(
        {
            "Date": ["2020-01-01"],
            "Open": [12.0],
            "High": [15.0],
            "Low": [11.9],
            "Close": [13.0],
            "Volume": [200],
        }
    )
    dtypes = {
        "Date": "object",
        "Open": "float64",
        "High": "float64",
        "Low": "float64",
        "Close": "float64",
        "Volume": "int64",
    }

    result = check_column_type(data, dtypes)
    assert result is True


def test_check_column_type_wrong_input():
    """
    Verify check_column_type returns False when at least one column
    has an incorrect data type.
    """
    data = pd.DataFrame(
        {
            "Date": ["2020-01-01"],
            "Open": [12.0],
            "High": ["15.0"],
            "Low": [11.9],
            "Close": [13.0],
            "Volume": [200],
        }
    )
    dtypes = {
        "Date": "float",
        "Open": "float64",
        "High": "float64",
        "Low": "float64",
        "Close": "float64",
        "Volume": "int64",
    }

    result = check_column_type(data, dtypes)
    assert result is False


def test_check_corrupted_values_right_input():
    """
    Verify check_corrupted_values returns True when the DataFrame
    contains no null or negative numeric values.
    """

    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2020-01-01"]),
            "Open": [12.0],
            "High": [15.0],
            "Low": [11.9],
            "Close": [13.0],
            "Volume": [200],
        }
    )
    result = check_corrupted_values(data)
    assert result is True


def test_check_corrupted_values_wrong_input():
    """
    Verify check_corrupted_values returns False when null or
    negative numeric values are present.
    """
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2020-01-01"]),
            "Open": [12.0],
            "High": [None],
            "Low": [11.9],
            "Close": [13.0],
            "Volume": [200],
        }
    )
    result = check_corrupted_values(data)
    assert result is False


def test_check_logical_consistency_right_input():
    """
    Verify check_logical_consistency returns True when Low is the
    minimum and High is the maximum price in each row.
    """
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2020-01-01"]),
            "Open": [12.0],
            "High": [15.0],
            "Low": [11.9],
            "Close": [13.0],
            "Volume": [200],
        }
    )
    result = check_logical_consistency(data)
    assert result is True


def test_check_logical_consistency_wrong_input():
    """
    Verify check_logical_consistency returns False when price
    relationships are logically inconsistent.
    """

    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2020-01-01"]),
            "Open": [10.0],
            "High": [12.0],
            "Low": [11.9],
            "Close": [13.0],
            "Volume": [200],
        }
    )
    result = check_logical_consistency(data)
    assert result is False
