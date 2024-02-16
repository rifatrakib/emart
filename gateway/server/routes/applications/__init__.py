from fastapi import APIRouter

from server.routes.applications.apps import create_oauth_applications_router
from server.utils.enums import Versions
from server.utils.helpers import create_tags


def create_applications_router() -> APIRouter:
    router = APIRouter(prefix="/v1", tags=create_tags([Versions.version_1]))
    router.include_router(create_oauth_applications_router())
    return router
