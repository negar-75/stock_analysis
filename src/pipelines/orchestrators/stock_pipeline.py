import pandas as pd
from src.pipelines.validators.data_validator import data_validation
from src.pipelines.transformers.data_cleaner import clean_data
from src.pipelines.transformers.feature_engineer import FeatureEngineering


class StockDataPipeline:
    def __init__(self, dtypes, raw_data, volatility_window, moving_window):
        self.dtypes = dtypes
        self.data = raw_data
        self.volatility_window = volatility_window
        self.moving_window = moving_window

    def validate(self):
        if not data_validation(self.data, self.dtypes):
            raise ValueError("Validation failed")
        return self

    def clean(self):
        self.data = clean_data(self.data)
        return self

    def engineer_features(self):
        engineered_data = FeatureEngineering(
            self.data, self.volatility_window, self.moving_window
        )
        self.data = engineered_data.run()
        return self

    def run(self) -> pd.DataFrame:
        self.validate().clean().engineer_features()
        return self.data
