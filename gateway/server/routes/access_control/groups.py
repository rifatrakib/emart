from typing import Union

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session
from server.database.access_control.create import create_group
from server.database.access_control.delete import delete_group, remove_permission_from_group, remove_role_from_group
from server.database.access_control.read import filter_groups
from server.database.access_control.update import add_permission_to_group, add_role_to_group, update_group
from server.models.schemas.requests.access_control import GroupCreateSchema, GroupUpdateSchema
from server.models.schemas.responses.access_control import GroupResponse
from server.utils.exceptions import handle_422_unprocessable_entity


def create_groups_router() -> APIRouter:
    router = APIRouter(prefix="/groups")

    @router.post("", response_model=GroupResponse)
    async def create_new_group(
        payload: GroupCreateSchema,
        session: AsyncSession = Depends(get_database_session),
    ) -> GroupResponse:
        try:
            return await create_group(session, payload)
        except Exception as e:
            raise e

    @router.get("", response_model=list[GroupResponse])
    async def read_groups(
        page: int = Query(1, ge=1),
        role: Union[str, None] = Query(None),
        object_name: Union[str, None] = Query(None),
        action: Union[str, None] = Query(None),
        session: AsyncSession = Depends(get_database_session),
    ) -> list[GroupResponse]:
        try:
            if action and not object_name:
                raise handle_422_unprocessable_entity("Action requires object name")
            return await filter_groups(session, page, role, object_name, action)
        except Exception as e:
            raise e

    @router.patch("/{group_id}", response_model=GroupResponse)
    async def modify_group(
        group_id: int,
        payload: GroupUpdateSchema,
        session: AsyncSession = Depends(get_database_session),
    ) -> GroupResponse:
        try:
            return await update_group(session, group_id, payload)
        except Exception as e:
            raise e

    @router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def remove_group(
        group_id: int,
        session: AsyncSession = Depends(get_database_session),
    ) -> None:
        try:
            await delete_group(session, group_id)
        except Exception as e:
            raise e

    @router.post("/{group_id}/roles/{role_id}", response_model=GroupResponse)
    async def add_group_role(
        group_id: int,
        role_id: int,
        session: AsyncSession = Depends(get_database_session),
    ) -> GroupResponse:
        try:
            return await add_role_to_group(session, group_id, role_id)
        except Exception as e:
            raise e

    @router.delete("/{group_id}/roles/{role_id}", response_model=GroupResponse)
    async def revoke_group_role(
        group_id: int,
        role_id: int,
        session: AsyncSession = Depends(get_database_session),
    ) -> GroupResponse:
        try:
            return await remove_role_from_group(session, group_id, role_id)
        except Exception as e:
            raise e

    @router.post("/{group_id}/permissions/{permission_id}", response_model=GroupResponse)
    async def add_group_permission(
        group_id: int,
        permission_id: int,
        session: AsyncSession = Depends(get_database_session),
    ) -> GroupResponse:
        try:
            return await add_permission_to_group(session, group_id, permission_id)
        except Exception as e:
            raise e

    @router.delete("/{group_id}/permissions/{permission_id}", response_model=GroupResponse)
    async def revoke_group_permission(
        group_id: int,
        permission_id: int,
        session: AsyncSession = Depends(get_database_session),
    ) -> GroupResponse:
        try:
            return await remove_permission_from_group(session, group_id, permission_id)
        except Exception as e:
            raise e

    return router
