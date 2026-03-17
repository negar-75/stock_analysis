from sqlalchemy.ext.asyncio import create_async_engine

from stock_analysis.core.config import get_settings


engine = None


def get_engine():
    global engine
    if engine is None:
        engine = create_async_engine(get_settings().database_url)
    return engine
