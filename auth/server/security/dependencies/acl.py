from aioredis.client import Redis
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from server.database.cache.manager import read_from_cache
from server.models.schemas.out.auth import TokenUser
from server.security.authentication.jwt import decode_jwt
from server.security.dependencies.clients import get_redis_client
from server.utils.exceptions import raise_401_unauthorized

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
