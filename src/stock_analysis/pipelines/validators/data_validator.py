"""
Data validation module for stock price data.

Provides validation functions to ensure data quality before processing.
"""

import logging

import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
    is_object_dtype,
)

logger = logging.getLogger(__name__)

TYPE_CHECKS = {
    "datetime": is_datetime64_any_dtype,
    "float": is_float_dtype,
    "int": is_integer_dtype,
    "object": is_object_dtype,
}


def required_columns_exist(data: pd.DataFrame, columns_list: list) -> bool:
    """
    Check if all required columns exist in the DataFrame.

    Args:
        data (pd.DataFrame): Input DataFrame.
        columns_list (list): List of required column names.

    Returns:
        bool: True if all columns exist, False otherwise.
    """
    for col in columns_list:
        if col not in data.columns:
            logger.warning("Column '%s' does not exist", col)
            return False
    return True


def check_column_type(data: pd.DataFrame, columns_type: dict) -> bool:
    """
    Check if each column in the DataFrame matches the expected data type.

    Args:
        data (pd.DataFrame): Input DataFrame.
        columns_type (dict): Dictionary mapping column names to expected dtypes.

    Returns:
        bool: True if all columns have correct types, False otherwise.
    """
    for col, expected in columns_type.items():
        checker = next(
            (func for key, func in TYPE_CHECKS.items() if expected.startswith(key)),
            None,
        )

        if checker is None or not checker(data[col]):
            logger.warning(
                "Data type is wrong in column '%s', current type is %s",
                col,
                data[col].dtype,
            )
            return False

    return True


def check_corrupted_values(data: pd.DataFrame) -> bool:
    """
    Check for null or negative values in the DataFrame.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        bool: False if any null or negative value exists, True otherwise.
    """
    for col in data.columns:
        if pd.isnull(data[col]).any():
            logger.warning("Column '%s' has null values", col)
            return False
    numeric_cols = data.select_dtypes(include=["number"]).columns
    for num_cols in numeric_cols:
        if (data[num_cols] < 0).any():
            logger.warning("Column '%s' has negative values", num_cols)
            return False
    return True


def check_logical_consistency(data: pd.DataFrame) -> bool:
    """
    Ensure that 'Low' is the minimum and 'High' is the maximum for each row.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        bool: True if all rows are logically consistent, False otherwise.
    """
    lowest = data[["Open", "Close", "High", "Low"]].min(axis=1)
    highest = data[["Open", "Close", "High", "Low"]].max(axis=1)

    if not (lowest == data["Low"]).all():
        logger.warning("Low is not the minimum price in the row")
        return False
    if not (highest == data["High"]).all():
        logger.warning("High is not the maximum price in the row")
        return False
    return True


def data_validation(data: pd.DataFrame, dtypes: dict) -> bool:
    """
    Orchestrate all data validation checks:
    - Required columns exist
    - Column types are correct
    - No corrupted values
    - Logical consistency of High/Low values

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        bool: True if all checks pass, False otherwise.
    """

    if not required_columns_exist(data, dtypes.keys()):
        return False
    if not check_column_type(data, dtypes):
        return False
    if not check_corrupted_values(data):
        return False
    if not check_logical_consistency(data):
        return False
    return True
