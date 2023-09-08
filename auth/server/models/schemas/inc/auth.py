from pydantic import EmailStr
from server.models.schemas.base import BaseRequestSchema


class LoginRequestSchema(BaseRequestSchema):
    username: str
    password: str


class SignupRequestSchema(LoginRequestSchema):
    email: EmailStr


class PasswordChangeRequestSchema(BaseRequestSchema):
    current_password: str
    new_password: str
