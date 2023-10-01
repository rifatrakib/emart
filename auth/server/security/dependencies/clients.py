from typing import Type

import aioredis
from aioredis.client import Redis
from fastapi import Path
from fastapi_sso.sso.base import SSOBase
from server.config.factory import settings
from server.models.database import get_async_database_session
from server.security.authentication.sso import sso_clients
from server.utils.enums import Provider
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


async def get_sso_client(provider: Provider = Path()) -> Type[SSOBase]:
    if provider == Provider.google:
        return sso_clients.google
    if provider == Provider.microsoft:
        return sso_clients.microsoft
    if provider == Provider.github:
        return sso_clients.github
    if provider == Provider.facebook:
        return sso_clients.facebook
