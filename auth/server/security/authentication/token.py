from datetime import datetime, timedelta
from typing import Any, Dict

from aioredis.client import Redis
from jose import JWTError, jwt
from pydantic import ValidationError
from server.config.factory import settings
from server.database.cache.manager import write_data_to_cache
from server.models.database.users import Account
from server.models.schemas.out.auth import TokenCollectionSchema, TokenUser
from server.utils.enums import TimeUnits


class JWTGenerator:
    def __init__(self, unit: TimeUnits):
        # secret keys
        self.access_token_secret_key = settings.JWT_SECRET_KEY
        self.refresh_token_secret_key = settings.REFRESH_TOKEN_SECRET_KEY

        # algorithms
        self.access_token_algorithm = settings.JWT_ALGORITHM
        self.refresh_token_algorithm = settings.REFRESH_TOKEN_ALGORITHM

        # subjects
        self.access_token_subject = settings.JWT_SUBJECT
        self.refresh_token_subject = settings.REFRESH_TOKEN_SUBJECT

        # time units
        if unit == TimeUnits.days:
            access_token_expiry = timedelta(seconds=settings.JWT_DAY)
            refresh_token_expiry = timedelta(seconds=settings.REFRESH_TOKEN_DAY)
        elif unit == TimeUnits.hours:
            access_token_expiry = timedelta(seconds=settings.JWT_HOUR)
            refresh_token_expiry = timedelta(seconds=settings.REFRESH_TOKEN_HOUR)
        else:
            access_token_expiry = timedelta(seconds=settings.JWT_MIN)
            refresh_token_expiry = timedelta(seconds=settings.REFRESH_TOKEN_MIN)

        self.access_token_expiry = datetime.utcnow() + access_token_expiry
        self.refresh_token_expiry = datetime.utcnow() + refresh_token_expiry

    def create_access_token(self, data: TokenUser) -> str:
        return jwt.encode(
            {
                **data.model_dump(),
                "exp": self.access_token_expiry,
                "sub": self.access_token_subject,
            },
            key=self.access_token_secret_key,
            algorithm=self.access_token_algorithm,
        )

    def create_refresh_token(self, data: TokenUser) -> str:
        return jwt.encode(
            {
                **data.model_dump(),
                "exp": self.refresh_token_expiry,
                "sub": self.refresh_token_subject,
            },
            key=self.refresh_token_secret_key,
            algorithm=self.refresh_token_algorithm,
        )

    def identify_user(self, payload: Dict[str, Any]) -> TokenUser:
        return TokenUser(
            id=payload.get("id"),
            username=payload.get("username"),
            email=payload.get("email"),
            is_active=payload.get("is_active"),
            open_id=payload.get("open_id"),
            provider=payload.get("provider"),
        )

    def decode_access_token(self, token: str) -> TokenUser:
        try:
            payload = jwt.decode(
                token=token,
                key=self.access_token_secret_key,
                algorithms=[self.access_token_algorithm],
            )
            return self.identify_user(payload)
        except JWTError:
            raise ValueError("unable to decode JWT")
        except ValidationError:
            raise ValueError("invalid payload in JWT")

    def decode_refresh_token(self, token: str) -> TokenUser:
        try:
            payload = jwt.decode(
                token=token,
                key=self.refresh_token_secret_key,
                algorithms=[self.refresh_token_algorithm],
            )
            return self.identify_user(payload)
        except JWTError:
            raise ValueError("unable to decode JWT")
        except ValidationError:
            raise ValueError("invalid payload in JWT")

    async def generate_jwt(self, redis: Redis, user: Account) -> TokenCollectionSchema:
        token_data = TokenUser(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            open_id=user.open_id,
            provider=user.provider,
        )

        access_token = self.create_access_token(token_data)
        refresh_token = self.create_refresh_token(token_data)
        await write_data_to_cache(redis, access_token, refresh_token)

        return TokenCollectionSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )
