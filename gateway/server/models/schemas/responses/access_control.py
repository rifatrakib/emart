from pydantic import Field

from server.models.schemas.responses import BaseResponseSchema


class PermissionResponse(BaseResponseSchema):
    object_name: str
    action: str


class GroupResponse(BaseResponseSchema):
    title: str
    roles: list["RoleResponse"] = Field(default_factory=list)


class RoleResponse(BaseResponseSchema):
    title: str
    permissions: list["PermissionResponse"] = Field(default_factory=list)
