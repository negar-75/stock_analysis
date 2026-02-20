from stock_analysis.db.engine import get_engine
from sqlalchemy.orm import sessionmaker


engine = get_engine("prod")

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
