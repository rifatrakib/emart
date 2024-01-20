from typing import Union

from pydantic import Field

from server.models.schemas.requests import BaseRequestSchema


class PermissionCreateSchema(BaseRequestSchema):
    object_name: str
    action: str


class PermissionUpdateSchema(BaseRequestSchema):
    object_name: Union[str, None] = None
    action: Union[str, None] = None


class GroupCreateSchema(BaseRequestSchema):
    title: str
    permissions: list[PermissionCreateSchema] = Field(default_factory=list)


class GroupUpdateSchema(BaseRequestSchema):
    title: Union[str, None] = None


class RoleCreateSchema(BaseRequestSchema):
    title: str
    permissions: list[PermissionCreateSchema] = Field(default_factory=list)


class RoleUpdateSchema(BaseRequestSchema):
    title: Union[str, None] = None
