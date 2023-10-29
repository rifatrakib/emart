from functools import lru_cache
from typing import Type

import aioredis
from aioredis.client import Redis
from elasticapm.base import Client
from elasticapm.contrib.starlette import make_apm_client
from fastapi import Path
from fastapi_sso.sso.base import SSOBase
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.models.database import get_async_database_session
from server.security.authentication.sso import sso_clients
from server.utils.enums import Provider


@lru_cache
def get_elastic_apm_client() -> Client:
    return make_apm_client(
        {
            "SERVICE_NAME": settings.APP_NAME,
            "SECRET_TOKEN": settings.ELASTIC_APM_SECRET_TOKEN,
            "SERVER_URL": settings.ELASTIC_APM_SERVER_URL,
            "ENVIRONMENT": settings.MODE,
            "LOG_LEVEL": "debug",
        }
    )


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
