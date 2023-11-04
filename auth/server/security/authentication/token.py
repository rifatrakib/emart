from typing import Union

import aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.database.cache.manager import remove_from_cache
from server.database.token.crud import remove_token, update_access_token, write_tokens
from server.models.database import get_async_database_session
from server.models.database.users import Account
from server.models.schemas.out.auth import TokenCollectionSchema, TokenUser


async def store_tokens(tokens: TokenCollectionSchema, user: Union[Account, TokenUser]):
    session: AsyncSession = get_async_database_session()
    await write_tokens(session, user.id, tokens)
    await session.close()


async def update_tokens(old_access_token: str, new_access_token: str, refresh_token: str):
    session: AsyncSession = get_async_database_session()
    await update_access_token(session, old_access_token, new_access_token)
    await session.close()

    redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
    await remove_from_cache(redis, old_access_token)
    await redis.close()


async def cleanup_tokens(access_token: str):
    session: AsyncSession = get_async_database_session()
    await remove_token(session, access_token)
    await session.close()

    redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
    await remove_from_cache(redis, access_token)
    await redis.close()
