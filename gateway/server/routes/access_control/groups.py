from typing import Union

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session
from server.database.access_control.create import create_group
from server.database.access_control.read import filter_groups
from server.models.schemas.requests.access_control import GroupCreateSchema
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

    return router
