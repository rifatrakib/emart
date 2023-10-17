from typing import Union

from aioredis.client import Redis
from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from server.database.cache.manager import read_token_from_cache
from server.database.user.auth import read_user_by_email
from server.models.schemas.out.auth import TokenUser
from server.security.authentication.jwt import decode_access_token
from server.security.dependencies.clients import get_database_session, get_redis_client
from server.utils.exceptions import raise_401_unauthorized
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


async def get_access_token(token: str = Depends(oauth2_scheme)) -> str:
    return token


async def get_refresh_token(
    redis: Redis = Depends(get_redis_client),
    token: str = Depends(get_access_token),
) -> str:
    try:
        refresh_token = await read_token_from_cache(redis, token)
        if not refresh_token:
            raise_401_unauthorized("Please log in again.")

        return refresh_token
    except HTTPException:
        raise_401_unauthorized("Please log in again.")


def authenticate_active_user(token: str = Depends(oauth2_scheme)) -> TokenUser:
    try:
        user_data: TokenUser = decode_access_token(token)
        return user_data
    except ValueError:
        raise_401_unauthorized("Invalid token")


async def is_superuser(
    session: AsyncSession = Depends(get_database_session),
    auth_token: Union[str, None] = Cookie(default=None),
) -> Union[TokenUser, None]:
    if not auth_token:
        return None

    try:
        user_data: TokenUser = decode_access_token(auth_token)
        admin = await read_user_by_email(session=session, email=user_data.email)
        if admin.is_superuser:
            return user_data
        return None
    except ValueError:
        return None
