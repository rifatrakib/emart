from datetime import datetime
from typing import Union

from pydantic import EmailStr, Field

from server.models.schemas.responses import BaseResponseSchema
from server.models.schemas.responses.access_control import GroupResponse, PermissionResponse, RoleResponse
from server.utils.enums import Gender


class AccountResponse(BaseResponseSchema):
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
