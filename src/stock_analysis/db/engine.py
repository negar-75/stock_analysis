from sqlalchemy.ext.asyncio import create_async_engine

from stock_analysis.core.config import settings


engine = create_async_engine(settings.database_url)
