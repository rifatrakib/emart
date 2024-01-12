from fastapi import APIRouter

from server.config.factory import settings
from server.utils.enums import Tags, Versions
from server.utils.helpers import create_tags


def create_health_check_router():
    router = APIRouter(prefix="/v1", tags=create_tags([Tags.health_check, Versions.version_1]))

    @router.get("/health")
    async def health_check():
        return {"app_name": f"{settings.APP_NAME} is running on {settings.MODE} environment"}

    return router
