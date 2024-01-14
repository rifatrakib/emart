from pydantic import EmailStr, validator

from server.models.schemas.requests import BaseRequestSchema
from server.utils.exceptions import handle_422_unprocessable_entity
from server.utils.helpers import validate_password


class SignupRequestSchema(BaseRequestSchema):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @validator("password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        try:
            return validate_password(v)
        except ValueError as e:
            raise handle_422_unprocessable_entity(e.args[0])
