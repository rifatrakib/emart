from fastapi import APIRouter

from server.models.schemas.responses.access_control import GroupResponse


def create_groups_router() -> APIRouter:
    router = APIRouter(prefix="/groups")

    @router.post("", response_model=GroupResponse)
    async def create_new_group() -> GroupResponse:
        pass

    return router
