import pandas as pd


def sort_by_column(data: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Sort a DataFrame by a specified column.

    Args:
        data (pd.DataFrame): Input DataFrame.
        col_name (str): Column name to sort by.

    Returns:
        pd.DataFrame: Sorted DataFrame.
    """
    return data.sort_values(by=f"{col_name}")


def convert_to_datetime(data: pd.DataFrame, col_name: str):
    """
    Convert a column to pandas datetime format.

    Args:
        data (pd.DataFrame): Input DataFrame.
        col_name (str): Name of the column to convert.

    Returns:
        None: The DataFrame is modified in place.
    """
    try:
        data[f"{col_name}"] = pd.to_datetime(data[f"{col_name}"]).dt.date
        return True
    except (ValueError, TypeError) as e:
        print(f"Data conversion error :{e}")
        return False


def drop_duplicates(data: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Remove duplicate rows based on a specific column.

    Keeps the first occurrence of each unique value.

    Args:
        data (pd.DataFrame): Input DataFrame.
        col_name (str): Column used to identify duplicates.

    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """
    return data.drop_duplicates(subset=[f"{col_name}"], keep="first")


def col_name_normalization(data: pd.DataFrame) -> list[str]:
    """
    Normalize column names by converting them to lowercase
    and replacing spaces with underscores.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        List[str]: Normalized column names.
    """
    return [col.lower().replace(" ", "_") for col in data.columns]


def col_ordering(data: pd.DataFrame, order: list):
    """
    Reorder DataFrame columns based on a specified order.

    Args:
        data (pd.DataFrame): Input DataFrame.
        order (list): Desired column order.

    Returns:
        pd.DataFrame: DataFrame with reordered columns.
    """
    return data[order]


def clean_data(data: pd.DataFrame):
    """
    Perform data cleaning operations after validation.

    Cleaning steps include:
    - Normalizing column names
    - Sorting data by date
    - Removing duplicate dates
    - Selecting and ordering required columns

    Assumes that data has already passed validation checks.

    Args:
        data (pd.DataFrame): Validated input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame ready for feature engineering.
    """
    data.columns = col_name_normalization(data)
    convert_to_datetime(data, "date")
    data = drop_duplicates(data, "date")
    data = sort_by_column(data, "date")

    # extra column will be removed in below section
    data = col_ordering(
        data, ["date", "open", "high", "low", "close", "adj_close", "volume"]
    )
    return data
