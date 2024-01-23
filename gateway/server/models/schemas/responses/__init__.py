from typing import Union

from server.models.schemas import BaseSchema


class BaseResponseSchema(BaseSchema):
    pass


class HealthResponseSchema(BaseResponseSchema):
    APP_NAME: str
    MODE: str
    DEBUG: bool


class MessageResponseSchema(BaseResponseSchema):
    msg: str
    loc: Union[list[str], None] = None
    type: Union[str, None] = None
