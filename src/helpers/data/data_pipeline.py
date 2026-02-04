import pandas as pd
from src.helpers.data.data_validation import load_data, data_validation
from src.helpers.data.data_cleaner import clean_data


class DataAnalyze:
    def __init__(self, dtypes, raw_data):
        self.dtypes = dtypes
        self.data = raw_data

    def validate(self):
        if not data_validation(self.data, self.dtypes):
            raise ValueError("Validation failed")
        return self

    def transform(self):
        self.data = clean_data(self.data)
        return self

    def run(self):
        self.validate().transform()
        return self.data
