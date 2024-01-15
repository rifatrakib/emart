from sqlalchemy.ext.asyncio import AsyncSession

from server.database.accounts.read import read_tokens


async def update_access_token(session: AsyncSession, old_access_token: str, new_access_token: str):
    tokens = await read_tokens(session, old_access_token)
    if tokens:
        tokens.access_token = new_access_token
        await session.commit()
