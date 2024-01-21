from typing import Union

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session
from server.database.access_control.create import create_role
from server.database.access_control.delete import delete_role, remove_permission_from_role
from server.database.access_control.read import filter_roles
from server.database.access_control.update import add_permission_to_role, update_role
from server.models.schemas.requests.access_control import RoleCreateSchema, RoleUpdateSchema
from server.models.schemas.responses.access_control import RoleResponse
from server.utils.exceptions import handle_422_unprocessable_entity


def create_roles_router() -> APIRouter:
    router = APIRouter(prefix="/roles")

    @router.post("", response_model=RoleResponse)
    async def create_new_role(
        payload: RoleCreateSchema,
        session: AsyncSession = Depends(get_database_session),
    ) -> RoleResponse:
        try:
            return await create_role(session, payload)
        except Exception as e:
            raise e

    @router.get("", response_model=list[RoleResponse])
    async def read_roles(
        page: int = Query(1, ge=1),
        group: Union[str, None] = Query(None),
        object_name: Union[str, None] = Query(None),
        action: Union[str, None] = Query(None),
        session: AsyncSession = Depends(get_database_session),
    ) -> list[RoleResponse]:
        try:
            if action and not object_name:
                raise handle_422_unprocessable_entity("Action requires object name")
            return await filter_roles(session, page, group, object_name, action)
        except Exception as e:
            raise e

    @router.patch("/{role_id}", response_model=RoleResponse)
    async def modify_permission(
        role_id: int,
        payload: RoleUpdateSchema,
        session: AsyncSession = Depends(get_database_session),
    ) -> RoleResponse:
        try:
            return await update_role(session, role_id, payload)
        except Exception as e:
            raise e

    @router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def remove_role(
        role_id: int,
        session: AsyncSession = Depends(get_database_session),
    ) -> None:
        try:
            await delete_role(session, role_id)
        except Exception as e:
            raise e

    @router.put("/{role_id}/permissions", response_model=RoleResponse)
    async def add_role_permission(
        role_id: int,
        object_name: Union[str, None] = Query(default=None, title="Object Name"),
        action: Union[str, None] = Query(default=None, title="Action"),
        session: AsyncSession = Depends(get_database_session),
    ) -> RoleResponse:
        try:
            if not object_name or not action:
                raise handle_422_unprocessable_entity("One of object name and action required")
            return await add_permission_to_role(session, role_id, object_name, action)
        except Exception as e:
            raise e

    @router.patch("/{role_id}/permissions", response_model=RoleResponse)
    async def revoke_role_permission(
        role_id: int,
        object_name: Union[str, None] = Query(default=None, title="Object Name"),
        action: Union[str, None] = Query(default=None, title="Action"),
        session: AsyncSession = Depends(get_database_session),
    ) -> RoleResponse:
        try:
            if not object_name or not action:
                raise handle_422_unprocessable_entity("One of object name and action required")
            return await remove_permission_from_role(session, role_id, object_name, action)
        except Exception as e:
            raise e

    return router
