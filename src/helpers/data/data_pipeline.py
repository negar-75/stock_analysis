import pandas as pd
from src.helpers.data.data_validation import load_data, data_validation
from src.helpers.data.data_cleaner import clean_data
from src.db.query import read_db_by_col, write_csv_to_db


class DataAnalyze:
    def __init__(self, file_path, table_name, dtypes):
        self.file_path = file_path
        self.table_name = table_name
        self.dtypes = dtypes

    def extract(self):
        self.data = load_data(self.file_path)
        return self

    def validate(self):
        if not data_validation(self.data, self.dtypes):
            raise ValueError("Validation failed")
        return self

    def transform(self):
        self.data = clean_data(self.data)
        return self.data

    # def load_to_db(self):
    #     existing_dates = set(read_db_by_col("date", self.table_name)["date"])
    #     new_rows = self.data[~self.data["date"].isin(existing_dates)]

    #     if not new_rows.empty:
    #         write_csv_to_db(new_rows)
    #     return len(new_rows)

    def run(self):
        return self.extract().validate().transform()
