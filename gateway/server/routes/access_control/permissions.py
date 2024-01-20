from typing import Union

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session
from server.database.access_control.create import create_permission
from server.database.access_control.delete import delete_permission
from server.database.access_control.read import filter_permissions
from server.database.access_control.update import update_permissions
from server.models.schemas.requests.access_control import PermissionCreateSchema, PermissionUpdateSchema
from server.models.schemas.responses.access_control import PermissionResponse
from server.utils.exceptions import handle_422_unprocessable_entity


def create_permissions_router() -> APIRouter:
    router = APIRouter(prefix="/permissions")

    @router.post("", response_model=PermissionResponse)
    async def create_new_permission(
        payload: PermissionCreateSchema,
        session: AsyncSession = Depends(get_database_session),
    ) -> PermissionResponse:
        try:
            return await create_permission(session, payload)
        except Exception as e:
            raise e

    @router.get("", response_model=list[PermissionResponse])
    async def read_permissions(
        page: int = Query(1, ge=1),
        role: Union[str, None] = Query(None),
        group: Union[str, None] = Query(None),
        session: AsyncSession = Depends(get_database_session),
    ) -> list[PermissionResponse]:
        try:
            if role and group:
                raise handle_422_unprocessable_entity("Cannot filter by both role and group")
            return await filter_permissions(session, page, role, group)
        except Exception as e:
            raise e

    @router.patch("/{permission_id}", response_model=PermissionResponse)
    async def modify_permission(
        permission_id: int,
        payload: PermissionUpdateSchema,
        session: AsyncSession = Depends(get_database_session),
    ) -> PermissionResponse:
        try:
            if not payload.model_dump(exclude_unset=True):
                raise handle_422_unprocessable_entity("No fields to update")
            return await update_permissions(session, permission_id, payload)
        except Exception as e:
            raise e

    @router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def remove_permission(
        permission_id: int,
        session: AsyncSession = Depends(get_database_session),
    ) -> None:
        try:
            await delete_permission(session, permission_id)
        except Exception as e:
            raise e

    return router
