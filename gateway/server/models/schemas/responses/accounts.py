from datetime import datetime
from typing import Union

from pydantic import EmailStr, Field

from server.models.schemas import BaseSchema
from server.utils.enums import Gender


class PermissionResponse(BaseSchema):
    object_name: str
    action: str


class GroupResponse(BaseSchema):
    title: str
    roles: list["RoleResponse"] = Field(default_factory=list)


class RoleResponse(BaseSchema):
    title: str
    groups: list[GroupResponse] = Field(default_factory=list)
    permissions: list["PermissionResponse"] = Field(default_factory=list)


class AccountResponse(BaseSchema):
    username: str
    email: EmailStr
    first_name: str
    middle_name: Union[str, None] = None
    last_name: str
    birth_date: Union[datetime, None] = None
    gender: Union[Gender, None] = None
    address: Union[str, None] = None
    groups: list[GroupResponse] = Field(default_factory=list)
    roles: list[RoleResponse] = Field(default_factory=list)
    permissions: list[PermissionResponse] = Field(default_factory=list)
