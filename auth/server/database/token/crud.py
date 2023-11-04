from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.users import RefreshToken
from server.models.schemas.out.auth import TokenCollectionSchema


async def write_tokens(session: AsyncSession, account_id: int, tokens: TokenCollectionSchema):
    refresh_token = RefreshToken(
        refresh_token=tokens.refresh_token,
        access_token=tokens.access_token,
        account_id=account_id,
    )
    session.add(refresh_token)
    await session.commit()


async def read_tokens(session: AsyncSession, access_token: str) -> RefreshToken:
    stmt = select(RefreshToken).where(RefreshToken.access_token == access_token)
    query = await session.execute(stmt)
    token = query.scalar()
    return token


async def update_access_token(session: AsyncSession, old_access_token: str, new_access_token: str):
    tokens = await read_tokens(session, old_access_token)
    if tokens:
        tokens.access_token = new_access_token
        await session.commit()


async def remove_token(session: AsyncSession, access_token: str):
    tokens = await read_tokens(session, access_token)
    if tokens:
        await session.delete(tokens)
        await session.commit()
