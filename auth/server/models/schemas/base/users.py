from pydantic import EmailStr, Field
from server.models.schemas.base import BaseAPISchema
from server.models.schemas.base.fields import email_field, username_field


class UserBase(BaseAPISchema):
    username: str = username_field(Field)
    email: EmailStr = email_field(Field)
