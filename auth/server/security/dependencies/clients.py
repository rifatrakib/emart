import aioredis
from aioredis.client import Redis
from server.config.factory import settings


async def get_redis_client() -> Redis:
    try:
        redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
        return redis
    finally:
        await redis.close()
