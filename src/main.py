from helpers.data.data_pipeline import DataAnalyze
from helpers.features.features import FeatureEngineering

raw_path = "/Users/negarnasiri/Documents/python/stock_analysis/data/raw/OCFT.csv"
clean_path = "/Users/negarnasiri/Documents/python/stock_analysis/data/processed/OCFT_clean.csv"
types = {
    "Date": "object",
    "Open": "float64",
    "High": "float64",
    "Low": "float64",
    "Close": "float64",
    "Adj Close": "float64",
    "Volume": "int64",
}

if __name__ == "__main__":
    cleaned_data = DataAnalyze(raw_path, types,clean_path)
    processed_data = cleaned_data.run()
    analytic_data = FeatureEngineering(processed_data, 15, 5)
    df = analytic_data.run()
