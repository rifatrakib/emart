from typing import Union

from server.models.schemas.responses import BaseResponseSchema


class ApplicationResponse(BaseResponseSchema):
    id: int
    name: str
    description: Union[str, None] = None
    callback_url: str
    client_id: str
    secret_key: str
