import redis
import os

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL") or "redis://redis:6379/0", decode_responses=True)
