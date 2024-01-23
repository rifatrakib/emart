import aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.connections.clients import get_async_database_session
from server.database.accounts.create import write_tokens
from server.database.accounts.update import update_access_token
from server.database.cache import remove_from_cache
from server.models.database.accounts import Account
from server.models.schemas.responses.auth import TokenCollectionSchema


async def store_tokens(tokens: TokenCollectionSchema, user: Account):
    session: AsyncSession = get_async_database_session()
    await write_tokens(session, user.id, tokens)
    await session.close()


async def update_tokens(old_access_token: str, new_access_token: str):
    session: AsyncSession = get_async_database_session()
    await update_access_token(session, old_access_token, new_access_token)
    await session.close()

    redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
    await remove_from_cache(redis, old_access_token)
    await redis.close()
