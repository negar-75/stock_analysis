from helpers.data.data_pipeline import DataAnalyze
from helpers.features.features import FeatureEngineering

RAW_PATH = "data/raw/OCFT.csv"
RAW_PATH = "data/processed/OCFT_clean.csv"
ANALYTIC_PATH = "data/processed/OCFT_analytic.csv"

DTYPES = {
    "Date": "object",
    "Open": "float64",
    "High": "float64",
    "Low": "float64",
    "Close": "float64",
    "Adj Close": "float64",
    "Volume": "int64",
}

if __name__ == "__main__":
    cleaned_data = DataAnalyze(RAW_PATH, DTYPES,RAW_PATH)
    processed_data = cleaned_data.run()
    analytic_data = FeatureEngineering(processed_data, 15, 5)
    df = analytic_data.run()
