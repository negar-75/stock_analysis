from redis import Redis
import json


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get(self, key: str) -> dict | None:
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value: dict, ttl: int = 3600) -> None:
        self.redis.set(key, json.dumps(value), ex=ttl)

    def invalidate(self, key: str) -> None:
        self.redis.delete(key)
