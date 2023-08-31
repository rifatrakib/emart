import aioredis
from aioredis.client import Redis
from server.config.factory import settings
from server.models.database import get_async_database_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_redis_client() -> Redis:
    try:
        redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
        yield redis
    finally:
        await redis.close()


async def get_database_session() -> AsyncSession:
    try:
        session: AsyncSession = get_async_database_session()
        yield session
    finally:
        await session.close()
