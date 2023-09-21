from typing import Union

from pydantic import Field
from server.models.schemas.base.fields import name_field
from server.models.schemas.base.users import ProfileBase


class ProfileCreateSchema(ProfileBase):
    pass


class ProfileUpdateSchema(ProfileBase):
    first_name: Union[str, None] = Field(default=None, **name_field(place="first", max_length=64))
    last_name: Union[str, None] = Field(default=None, **name_field(place="last", max_length=64))
