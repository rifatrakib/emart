from pydantic import Field

from server.models.schemas.responses import BaseResponseSchema


class PermissionResponse(BaseResponseSchema):
    id: int
    object_name: str
    action: str


class RoleResponse(BaseResponseSchema):
    id: int
    title: str
    permissions: list[PermissionResponse] = Field(default_factory=list)


class GroupResponse(BaseResponseSchema):
    id: int
    title: str
    roles: list[RoleResponse] = Field(default_factory=list)
