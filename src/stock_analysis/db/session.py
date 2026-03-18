from sqlalchemy.ext.asyncio import async_sessionmaker

from stock_analysis.db.engine import get_engine

_session_maker = None


def get_session_maker():
    global _session_maker
    if _session_maker is None:
        _session_maker = async_sessionmaker(
            bind=get_engine(),
            expire_on_commit=False,
        )
    return _session_maker