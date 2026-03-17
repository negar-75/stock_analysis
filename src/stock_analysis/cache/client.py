import redis.asyncio as redis
from stock_analysis.core.config import get_settings

redis_client = redis.Redis.from_url(get_settings().redis_url, decode_responses=True)
