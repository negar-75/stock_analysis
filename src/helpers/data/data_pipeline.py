import pandas as pd
from src.helpers.data.data_validation import load_data, data_validation
from src.helpers.data.data_cleaner import clean_data
from src.db.query import read_db_by_col, write_csv_to_db


class DataAnalyze:
    def __init__(self, file_path, table_name, dtypes, path):
        self.file_path = file_path
        self.table_name = table_name
        self.dtypes = dtypes
        self.path = path

    def extract(self):
        self.data = load_data(self.file_path)
        return self

    def validate(self):
        if not data_validation(self.data, self.dtypes):
            raise ValueError("Validation failed")
        return self

    def transform(self):
        self.data = clean_data(self.data)
        return self

    def save_cleaned(self):
        self.data.to_csv(
            f"{self.path}",
            index=False,
        )
        return self

    def run(self):
        self.extract().validate().transform().save_cleaned()
        return self.data
