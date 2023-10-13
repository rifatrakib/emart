from datetime import datetime, timedelta

from jose import jwt
from server.config.factory import settings
from server.models.schemas.out.auth import TokenUser
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
