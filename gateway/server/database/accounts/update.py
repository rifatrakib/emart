from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.database.accounts.read import read_tokens
from server.models.database.accounts import Account
from server.models.schemas.requests.accounts import AccountUpdateSchema
from server.models.schemas.requests.password import PasswordChangeRequestSchema
from server.security.authentication.passlib import pwd_generator
from server.utils.exceptions import handle_401_unauthorized, handle_404_not_found


async def update_access_token(session: AsyncSession, old_access_token: str, new_access_token: str):
    tokens = await read_tokens(session, old_access_token)
    if tokens:
        tokens.access_token = new_access_token
        await session.commit()


async def update_password(session: AsyncSession, user_id: int, payload: PasswordChangeRequestSchema) -> None:
    stmt = select(Account).where(Account.id == user_id)
    query = await session.execute(stmt)
    user = query.scalar()

    if not pwd_generator.verify_password(user.hash_salt, payload.current_password, user.hashed_password):
        raise handle_401_unauthorized(message="Incorrect password.")

    user.set_hashed_password(
        hashed_password=pwd_generator.generate_hashed_password(
            hash_salt=user.hash_salt,
            new_password=payload.new_password,
        ),
    )

    session.add(user)
    await session.commit()


async def reset_password(session: AsyncSession, user_id: int, new_password: str) -> None:
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


async def update_email(session: AsyncSession, old_email: str, new_email: str) -> None:
    stmt = select(Account).where(Account.email == old_email)
    query = await session.execute(stmt)
    user = query.scalar()
    user.email = new_email
    session.add(user)
    await session.commit()


async def update_account(session: AsyncSession, user_id: int, payload: AccountUpdateSchema) -> Account:
    stmt = select(Account).where(Account.id == user_id)
    query = await session.execute(stmt)
    account = query.scalar()

    if not account:
        raise handle_404_not_found(msg="No account found")

    for field, update_value in payload.model_dump(exclude_unset=True).items():
        if field == "birth_date":
            account.set_birth_date(birth_date=update_value)
        elif field == "gender":
            account.set_gender(gender=update_value)
        else:
            setattr(account, field, update_value)

    await session.flush()
    await session.commit()
    await session.refresh(account)
    return account
