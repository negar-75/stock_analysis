import yfinance as yf


class Ingestion:

    def __init__(self, start_date, end_date, ticker):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.data = None

    def fetch(self):
        dat = yf.Ticker(self.ticker)
        self.data = dat.history(start=self.start_date, end=self.end_date, interval="1d")
        return self

    def drop_extra_columns(self):
        self.data = self.data.drop(["Dividends", "Stock Splits"], axis=1)
        return self

    def convert_index_to_col(self):
        self.data["Date"] = self.data.index
        return self

    def remove_index(self):
        self.data.reset_index(drop=True, inplace=True)
        return self

    def run(self):
        self.fetch().drop_extra_columns().convert_index_to_col().remove_index()
        return self.data
