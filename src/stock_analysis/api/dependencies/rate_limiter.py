from stock_analysis.cache import redis_client
from fastapi import HTTPException, Request
from stock_analysis.core.config import get_settings


async def rate_limiter(request: Request):
    ip = request.client.host
    key = f"rate_limit:{ip}"

    count = await redis_client.incr(key)

    if count == 1:
        await redis_client.expire(key, get_settings().rate_limit_window)
    if count > get_settings().rate_limit:
        raise HTTPException(status_code=429, detail="Rate limit exceed")
