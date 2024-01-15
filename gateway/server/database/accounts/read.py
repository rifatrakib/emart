from fastapi_sso.sso.base import OpenID
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.accounts import Account, RefreshToken
from server.models.schemas.requests.auth import SignupRequestSchema
from server.security.authentication.passlib import pwd_generator
from server.utils.exceptions import handle_401_unauthorized, handle_403_forbidden, handle_404_not_found


async def check_email_and_username_availabililty(session: AsyncSession, payload: SignupRequestSchema) -> bool:
    stmt = select(Account).where(or_(Account.email == payload.email, Account.username == payload.username))
    query = await session.execute(stmt)
    user = query.scalar()
    return user is None


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Account:
    stmt = select(Account).where(or_(Account.username == username, Account.email == username))
    query = await session.execute(stmt)
    user = query.scalar()

    if not user:
        raise handle_404_not_found(msg=f"The username {username} is not registered.")
    if not user.is_active:
        raise handle_403_forbidden(msg=f"The account for username {username} is not activated.")
    if not pwd_generator.verify_password(user.hash_salt, password, user.hashed_password):
        raise handle_401_unauthorized(msg="Incorrect credentials.")

    return user


async def read_sso_account(session: AsyncSession, payload: OpenID) -> Account:
    stmt = select(Account).where(
        Account.open_id == payload.id,
        Account.email == payload.email,
        Account._provider == payload.provider,
    )
    query = await session.execute(stmt)
    user = query.scalar()
    return user


async def read_tokens(session: AsyncSession, access_token: str) -> RefreshToken:
    stmt = select(RefreshToken).where(RefreshToken.access_token == access_token)
    query = await session.execute(stmt)
    token = query.scalar()
    return token
