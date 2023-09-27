from fastapi_sso.sso.base import OpenID
from server.models.database.users import Account
from server.utils.exceptions import raise_404_not_found, raise_409_conflict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def read_sso_user(session: AsyncSession, payload: OpenID) -> Account:
    stmt = select(Account).where(
        Account.email == payload.email,
        Account._provider == payload.provider,
    )
    query = await session.execute(stmt)
    user = query.scalar()

    if not user:
        raise_404_not_found(message=f"No account registered via {payload.provider} with {payload.email}.")

    return user


async def create_sso_user(session: AsyncSession, payload: OpenID) -> Account:
    try:
        new_account = Account(username=payload.id, email=payload.email, provider=payload.provider)
        session.add(instance=new_account)
        await session.commit()
        await session.refresh(instance=new_account)
        return new_account
    except IntegrityError:
        raise_409_conflict(message="username or email already exists")
