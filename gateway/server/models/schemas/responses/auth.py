from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr, Field

from server.models.schemas import BaseSchema


class TokenUser(BaseSchema):
    id: int
    username: Union[str, None] = None
    email: Union[EmailStr, None]
    is_active: bool
    open_id: Union[str, None] = None
    provider: Union[str, None] = None


class TokenData(TokenUser):
    exp: datetime
    sub: str
    scopes: list[str] = Field(default_factory=list)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str


class TokenCollectionSchema(BaseModel):
    access_token: str
    refresh_token: str
