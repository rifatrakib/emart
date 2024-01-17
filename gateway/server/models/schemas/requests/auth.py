from datetime import datetime
from typing import Union

from pydantic import EmailStr, validator

from server.models.schemas.requests import BaseRequestSchema
from server.utils.enums import Gender
from server.utils.exceptions import handle_422_unprocessable_entity
from server.utils.helpers import validate_password


class SignupRequestSchema(BaseRequestSchema):
    username: str
    email: EmailStr
    password: str
    first_name: str
    middle_name: Union[str, None] = None
    last_name: str
    birth_date: Union[datetime, None] = None
    gender: Union[Gender, None] = None
    address: Union[str, None] = None

    @validator("password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        try:
            return validate_password(v)
        except ValueError as e:
            raise handle_422_unprocessable_entity(e.args[0])
