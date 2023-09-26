from typing import Union

from aioredis.client import Redis
from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from server.database.cache.manager import read_from_cache
from server.database.user.auth import read_user_by_email
from server.models.schemas.out.auth import TokenUser
from server.security.authentication.jwt import decode_jwt
from server.security.dependencies.clients import get_database_session, get_redis_client
from server.utils.exceptions import raise_401_unauthorized
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


async def is_user_active(
    redis: Redis = Depends(get_redis_client),
    token: str = Depends(oauth2_scheme),
) -> TokenUser:
    user = await read_from_cache(redis, token)
    if user["is_active"]:
        return token

    raise_401_unauthorized("Inactive user")


def authenticate_active_user(token: str = Depends(is_user_active)) -> TokenUser:
    try:
        user_data: TokenUser = decode_jwt(token)
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
        user_data: TokenUser = decode_jwt(auth_token)
        admin = await read_user_by_email(session=session, email=user_data.email)
        if admin.is_superuser:
            return user_data
        return None
    except ValueError:
        return None
