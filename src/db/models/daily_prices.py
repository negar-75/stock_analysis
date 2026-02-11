from sqlalchemy import (
    Column,
    Integer,
    Date,
    Numeric,
    BigInteger,
    UniqueConstraint,
    VARCHAR,
)

from sqlalchemy.orm import declarative_base


# def create_col(col:str,table_name:str,engine):


Base = declarative_base()


class DailyPrices(Base):
    __tablename__ = "daily_prices"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True)
    ticker = Column(VARCHAR(10), nullable=False)
    open = Column(Numeric(10, 4), nullable=False)
    high = Column(Numeric(10, 4), nullable=False)
    low = Column(Numeric(10, 4), nullable=False)
    close = Column(Numeric(10, 4), nullable=False)
    volume = Column(BigInteger, nullable=False)
    daily_return = Column(Numeric(10, 4), nullable=True)
    log_return = Column(Numeric(10, 4), nullable=True)
    rolling_volatility = Column(Numeric(10, 4), nullable=True)
    moving_average = Column(Numeric(10, 4), nullable=True)
    absolute_range = Column(Numeric(10, 4), nullable=False)
    relative_range_on_open = Column(Numeric(10, 4), nullable=False)
    relative_range_on_close = Column(Numeric(10, 4), nullable=False)
    open_close_range = Column(Numeric(10, 4), nullable=False)
    upper_shadow = Column(Numeric(10, 4), nullable=False)
    lower_shadow = Column(Numeric(10, 4), nullable=False)

    __table_args__ = (
        UniqueConstraint("ticker", "date", name="uq_daily_prices_ticker_date"),
    )
