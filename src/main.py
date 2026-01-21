from helpers.data.data_pipeline import DataAnalyze
from helpers.features.features import FeatureEngineering

path = "/Users/negarnasiri/Documents/python/stock_analysis/data/raw/OCFT.csv"
types = {
    "Date": "object",
    "Open": "float64",
    "High": "float64",
    "Low": "float64",
    "Close": "float64",
    "Adj Close": "float64",
    "Volume": "int64",
}
table_name = "daily_prices"

if __name__ == "__main__":
    cleaned_data = DataAnalyze(path, table_name, types)
    processed_data = cleaned_data.run()
    analytic_data = FeatureEngineering(processed_data, 15, 5)
    df = analytic_data.run()
    df.to_csv(
        "/Users/negarnasiri/Documents/python/stock_analysis/data/processed/analytical_data.csv",
        index=False,
    )
