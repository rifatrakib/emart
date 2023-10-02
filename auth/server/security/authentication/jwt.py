from datetime import datetime, timedelta
from typing import Union

from aioredis.client import Redis
from jose import JWTError, jwt
from pydantic import ValidationError
from server.config.factory import settings
from server.database.cache.manager import write_data_to_cache
from server.models.database.users import Account
from server.models.schemas.out.auth import TokenData, TokenUser


def create_jwt(data: TokenUser, expires_delta: Union[datetime, None] = None) -> str:
    expires_delta = expires_delta if expires_delta else timedelta(minutes=settings.JWT_MIN)
    expire = datetime.utcnow() + expires_delta
    to_encode = TokenData(**data.model_dump(), exp=expire, sub=settings.JWT_SUBJECT)
    return jwt.encode(
        to_encode.model_dump(),
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_jwt(token: str) -> TokenUser:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_data = TokenUser(
            id=payload.get("id"),
            username=payload.get("username"),
            email=payload.get("email"),
            is_active=payload.get("is_active"),
            open_id=payload.get("open_id"),
            provider=payload.get("provider"),
        )
    except JWTError as token_decode_error:
        raise ValueError("unable to decode JWT") from token_decode_error
    except ValidationError as validation_error:
        raise ValueError("invalid payload in JWT") from validation_error
    return user_data


async def get_jwt(redis: Redis, user: Account):
    token_data = TokenUser(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        open_id=user.open_id,
        provider=user.provider,
    )
    token = create_jwt(token_data)

    await write_data_to_cache(
        redis,
        token,
        token_data.model_dump_json(),
        settings.JWT_MIN * 60,
    )
    return token
