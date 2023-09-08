from pydantic import EmailStr, Field
from server.models.schemas.base import BaseAPISchema
from server.models.schemas.base.fields import email_field, username_field


class UserBase(BaseAPISchema):
    username: str = Field(**username_field())
    email: EmailStr = Field(**email_field())
