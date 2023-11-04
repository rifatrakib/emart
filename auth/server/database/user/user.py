from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.users import Account
from server.models.schemas.inc.auth import PasswordChangeRequestSchema
from server.security.authentication.password import pwd_generator
from server.utils.exceptions import raise_401_unauthorized


async def update_password(
    session: AsyncSession,
    user_id: int,
    payload: PasswordChangeRequestSchema,
):
    stmt = select(Account).where(Account.id == user_id)
    query = await session.execute(stmt)
    user = query.scalar()

    if not pwd_generator.verify_password(user.hash_salt, payload.current_password, user.hashed_password):
        raise_401_unauthorized(message="Incorrect password.")

    user.set_hashed_password(
        hashed_password=pwd_generator.generate_hashed_password(
            hash_salt=user.hash_salt,
            new_password=payload.new_password,
        ),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)


async def reset_password(
    session: AsyncSession,
    user_id: int,
    new_password: str,
):
    stmt = select(Account).where(Account.id == user_id)
    query = await session.execute(stmt)
    user = query.scalar()

    user.set_hashed_password(
        hashed_password=pwd_generator.generate_hashed_password(
            hash_salt=user.hash_salt,
            new_password=new_password,
        ),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)


async def update_email(
    session: AsyncSession,
    user_id: int,
    new_email: EmailStr,
):
    stmt = select(Account).where(Account.id == user_id)
    query = await session.execute(stmt)
    user = query.scalar()

    user.email = new_email
    session.add(user)
    await session.commit()
    await session.refresh(user)
