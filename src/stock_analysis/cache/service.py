from redis import Redis
import json


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> dict | None:
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: dict, ttl: int = 3600) -> None:
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def invalidate(self, key: str) -> None:
        await self.redis.delete(key)
