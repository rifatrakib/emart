from fastapi import APIRouter, Depends

from server.routes.access_control.groups import create_groups_router
from server.routes.access_control.permissions import create_permissions_router
from server.routes.access_control.roles import create_roles_router
from server.security.dependencies.acl import verify_access
from server.utils.enums import Tags, Versions
from server.utils.helpers import create_tags


def create_access_control_router() -> APIRouter:
    router = APIRouter(
        prefix="/v1",
        dependencies=[Depends(verify_access(["all:create", "all:read", "all:update", "all:delete"]))],
        tags=create_tags([Tags.access_control, Versions.version_1]),
    )
    router.include_router(create_groups_router())
    router.include_router(create_roles_router())
    router.include_router(create_permissions_router())
    return router
