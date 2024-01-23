from datetime import datetime
from typing import Union

from server.models.schemas.requests import BaseRequestSchema
from server.utils.enums import Gender


class AccountUpdateSchema(BaseRequestSchema):
    first_name: Union[str, None] = None
    middle_name: Union[str, None] = None
    last_name: Union[str, None] = None
    birth_date: Union[datetime, None] = None
    gender: Union[Gender, None] = None
    address: Union[str, None] = None
