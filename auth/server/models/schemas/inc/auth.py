from pydantic import EmailStr, validator
from server.models.schemas.base import BaseRequestSchema
from server.utils.helper import validate_password


class LoginRequestSchema(BaseRequestSchema):
    username: str
    password: str


class SignupRequestSchema(LoginRequestSchema):
    email: EmailStr

    @validator("password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        return validate_password(v)


class PasswordChangeRequestSchema(BaseRequestSchema):
    current_password: str
    new_password: str

    @validator("new_password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        return validate_password(v)
