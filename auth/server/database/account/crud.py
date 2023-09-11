from pydantic import EmailStr
from server.models.database.users import Account
from server.models.schemas.inc.auth import PasswordChangeRequestSchema, SignupRequestSchema
from server.security.authentication.password import pwd_generator
from server.utils.exceptions import raise_401_unauthorized, raise_403_forbidden, raise_404_not_found, raise_409_conflict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_account(session: AsyncSession, payload: SignupRequestSchema) -> Account:
    try:
        new_account = Account(username=payload.username, email=payload.email)
        new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        new_account.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=new_account.hash_salt,
                new_password=payload.password,
            ),
        )

        session.add(instance=new_account)
        await session.commit()
        await session.refresh(instance=new_account)

        return new_account
    except IntegrityError:
        raise_409_conflict(message="username or email already exists")


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Account:
    stmt = select(Account).where(Account.username == username)
    query = await session.execute(stmt)
    user = query.scalar()

    if not user:
        raise_404_not_found(message=f"The username {username} is not registered.")

    if not user.is_active:
        raise_403_forbidden(message=f"The account for username {username} is not activated.")

    if not pwd_generator.verify_password(user.hash_salt, password, user.hashed_password):
        raise_401_unauthorized(message="Incorrect password.")

    return user


async def activate_user_account(session: AsyncSession, user_id: int) -> Account:
    user = await session.get(Account, user_id)

    if not user:
        raise_404_not_found(message=f"The user with id {user_id} is not registered.")

    user.is_active = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def read_user_by_email(session: AsyncSession, email: EmailStr) -> Account:
    stmt = select(Account).where(Account.email == email)
    query = await session.execute(stmt)
    user = query.scalar()

    if not user:
        raise_404_not_found(message=f"The email {email} is not registered.")

    return user


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
