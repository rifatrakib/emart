from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_async_database_session
from server.database.accounts.create import write_tokens
from server.models.database.accounts import Account
from server.models.schemas.responses.auth import TokenCollectionSchema


async def store_tokens(tokens: TokenCollectionSchema, user: Account):
    session: AsyncSession = get_async_database_session()
    await write_tokens(session, user.id, tokens)
    await session.close()
