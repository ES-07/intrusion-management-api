import redis.asyncio as redis
import os

async def init_redis_pool() -> redis.Redis:
    redis_pool = await redis.from_url(
        "redis://localhost:6379",
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_pool