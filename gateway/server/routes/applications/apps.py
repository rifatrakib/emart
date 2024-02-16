from fastapi import APIRouter

from server.models.schemas.responses import MessageResponseSchema
from server.utils.enums import Tags
from server.utils.helpers import create_tags


def create_oauth_applications_router() -> APIRouter:
    router = APIRouter(prefix="/apps", tags=create_tags([Tags.application]))

    @router.get("/health", response_model=MessageResponseSchema)
    async def health_check() -> dict:
        return {"msg": "Applications Router is healthy"}

    return router
