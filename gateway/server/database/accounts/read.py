from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.accounts import Account
from server.models.schemas.requests.auth import SignupRequestSchema


async def check_email_and_username_availabililty(session: AsyncSession, payload: SignupRequestSchema) -> bool:
    stmt = select(Account).where(or_(Account.email == payload.email, Account.username == payload.username))
    query = await session.execute(stmt)
    user = query.scalar()
    return user is None
