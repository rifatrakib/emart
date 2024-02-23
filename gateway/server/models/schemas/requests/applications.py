from typing import Union

from server.models.schemas.requests import BaseRequestSchema


class ApplicationCreateSchema(BaseRequestSchema):
    name: str
    description: Union[str, None] = None
    callback_url: str


class ApplicationUpdateSchema(BaseRequestSchema):
    name: Union[str, None] = None
    description: Union[str, None] = None
    callback_url: Union[str, None] = None
