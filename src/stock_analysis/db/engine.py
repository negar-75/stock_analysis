from sqlalchemy.ext.asyncio import create_async_engine

from stock_analysis.core.config import get_settings

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(get_settings().database_url)
    return _engine
