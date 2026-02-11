from src.db.engine import get_engine
from sqlalchemy.orm import sessionmaker


engine = get_engine("DB_NAME")

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
