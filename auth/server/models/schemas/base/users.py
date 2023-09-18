from datetime import date
from typing import Union

from pydantic import EmailStr, Field, validator
from server.models.schemas.base import BaseAPISchema
from server.models.schemas.base.fields import address_field, birth_date_field, email_field, gender_field, name_field, username_field
from server.utils.enums import Gender


class UserBase(BaseAPISchema):
    username: str = Field(**username_field())
    email: EmailStr = Field(**email_field())


class ProfileBase(BaseAPISchema):
    first_name: str = Field(**name_field(place="first", max_length=64))
    middle_name: Union[str, None] = Field(default=None, **name_field(place="middle", max_length=256))
    last_name: str = Field(**name_field(place="last", max_length=64))
    birth_date: Union[date, None] = Field(default=None, **birth_date_field())
    address: Union[str, None] = Field(default=None, **address_field())
    gender: Union[Gender, None] = Field(default=None, **gender_field())

    @validator("birth_date", pre=True)
    def validate_birth_date(cls, value: Union[str, None]) -> Union[date, None]:
        if value is None:
            return None
        if isinstance(value, date):
            return value
        return date.fromisoformat(value)
