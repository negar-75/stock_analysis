from src.helpers.data.data_pipeline import DataAnalyze
from src.helpers.features.features import FeatureEngineering
from src.db.query import write_data_to_db


def run_pipeline(dtypes, raw_data, engine):

    cleaned_data = DataAnalyze(dtypes, raw_data)
    processed_data = cleaned_data.run()
    print("Data has been validated and cleaned")
    analytic_data = FeatureEngineering(processed_data, 15, 5)
    df = analytic_data.run()
    print("Analytical process has been done")
    inserted_rows = write_data_to_db(df, engine)
    return inserted_rows
