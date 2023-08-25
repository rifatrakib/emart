import re

from pydantic import EmailStr, Field, validator
from server.models.schemas.base import BaseRequestSchema
from server.models.schemas.base.fields import email_field, password_field, username_field


class SignupRequestSchema(BaseRequestSchema):
    username: str = username_field(Field)
    email: EmailStr = email_field(Field)
    password: str = password_field(Field)

    @validator("password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must be between 8 and 64 characters long and contain at least one uppercase letter, one lowercase letter, one"
                " digit and one special character."
            )
