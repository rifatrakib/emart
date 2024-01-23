import aioredis
from aioredis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.connections import get_async_database_session


async def get_database_session() -> AsyncSession:
    try:
        session: AsyncSession = get_async_database_session()
        yield session
    finally:
        await session.close()


async def get_redis_client() -> Redis:
    try:
        redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
        yield redis
    finally:
        await redis.close()
