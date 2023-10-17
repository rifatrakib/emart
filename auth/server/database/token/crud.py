from server.models.database.users import RefreshToken
from server.models.schemas.out.auth import TokenCollectionSchema
from server.utils.exceptions import raise_401_unauthorized
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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

    if not token:
        raise_401_unauthorized("User not logged in.")

    return token


async def update_access_token(session: AsyncSession, old_access_token: str, new_access_token: str):
    tokens = await read_tokens(session, old_access_token)
    tokens.access_token = new_access_token
    await session.commit()


async def remove_token(session: AsyncSession, access_token: str):
    tokens = await read_tokens(session, access_token)
    await session.delete(tokens)
    await session.commit()
