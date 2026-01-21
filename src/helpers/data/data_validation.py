import pandas as pd


def load_data(file_name: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_name (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data.
    """
    return pd.read_csv(file_name)


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
            print("column existance issue")
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
    for col in data.columns:
        if data[f"{col}"].dtypes != columns_type[f"{col}"]:
            print(f"data type is wrong in column {col}")
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
        if pd.isnull(data[f"{col}"]).any():
            print(f"column {col} has null values")
            return False
    numeric_cols = data.select_dtypes(include=["number"]).columns
    for num_cols in numeric_cols:
        if (data[f"{num_cols}"] < 0).any():
            print(f"column {num_cols} has negative values")
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
    lowest = data[["Open", "Close", "High", "Low", "Adj Close"]].min(axis=1)
    highest = data[["Open", "Close", "High", "Low", "Adj Close"]].max(axis=1)

    if not (lowest == data["Low"]).all():
        print("Low is not the the minimum price in the row")
        return False
    if not (highest == data["High"]).all():
        print("High is not the the maximum price in the row")
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
