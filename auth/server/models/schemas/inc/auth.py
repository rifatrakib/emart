from pydantic import EmailStr, validator

from server.models.schemas.base import BaseRequestSchema
from server.utils.exceptions import raise_422_unprocessable_entity
from server.utils.helper import validate_password


class SignupRequestSchema(BaseRequestSchema):
    username: str
    email: EmailStr
    password: str

    @validator("password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        try:
            return validate_password(v)
        except ValueError as e:
            raise_422_unprocessable_entity(e.args[0])


class PasswordChangeRequestSchema(BaseRequestSchema):
    current_password: str
    new_password: str

    @validator("new_password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        try:
            return validate_password(v)
        except ValueError as e:
            raise_422_unprocessable_entity(e.args[0])
