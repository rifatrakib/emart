from datetime import datetime

from pydantic import BaseModel, Field
from server.models.schemas.base.users import UserBase


class TokenUser(UserBase):
    id: int = Field(
        title="user ID",
        decription="Unique ID that can be used to distinguish between users.",
    )
    is_active: bool = Field(
        title="user account activation status",
        description="A boolean value to determine if user account is activated or not.",
    )


class TokenData(TokenUser):
    exp: datetime = Field(
        title="expiry of token",
        decription="A timestamp definining tokens period of validity.",
    )
    sub: str = Field(
        title="OAuth2.0 token subject",
        decription="A string for subject of the token as per OAuth2.0 requirements.",
    )


class TokenResponseSchema(BaseModel):
    access_token: str = Field(
        title="access token",
        decription="A string for access token as per OAuth2.0 requirements.",
    )
    token_type: str = Field(
        title="token type",
        decription="A string for token type as per OAuth2.0 requirements.",
    )
