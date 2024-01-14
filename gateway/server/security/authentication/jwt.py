from datetime import datetime, timedelta
from typing import Union

from aioredis.client import Redis
from jose import jwt

from server.config.factory import settings
from server.database.cache import write_data_to_cache
from server.models.database.accounts import Account
from server.models.schemas.responses.auth import TokenCollectionSchema, TokenData, TokenUser


def create_access_token(data: TokenUser, expires_delta: Union[datetime, None] = None) -> str:
    expires_delta = expires_delta if expires_delta else timedelta(minutes=settings.JWT_MIN)
    expire = datetime.utcnow() + expires_delta
    to_encode = TokenData(**data.model_dump(), exp=expire, sub=settings.JWT_SUBJECT)
    return jwt.encode(
        to_encode.model_dump(),
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(data: TokenUser, expires_delta: Union[datetime, None] = None) -> str:
    expires_delta = expires_delta if expires_delta else timedelta(minutes=settings.REFRESH_TOKEN_MIN)
    expire = datetime.utcnow() + expires_delta
    to_encode = TokenData(**data.model_dump(), exp=expire, sub=settings.REFRESH_TOKEN_SUBJECT)
    return jwt.encode(
        to_encode.model_dump(),
        key=settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.REFRESH_TOKEN_ALGORITHM,
    )


async def get_jwt(redis: Redis, user: Account) -> TokenCollectionSchema:
    token_data = TokenUser(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        open_id=user.open_id,
        provider=user.provider,
    )
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    await write_data_to_cache(redis, access_token, refresh_token)
    return TokenCollectionSchema(access_token=access_token, refresh_token=refresh_token)
