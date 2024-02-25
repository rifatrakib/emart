from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session
from server.database.applications.create import create_new_application
from server.database.applications.read import read_applications
from server.database.applications.update import update_application
from server.models.schemas.requests.applications import ApplicationCreateSchema, ApplicationUpdateSchema
from server.models.schemas.responses import MessageResponseSchema
from server.models.schemas.responses.applications import ApplicationResponse
from server.models.schemas.responses.auth import TokenUser
from server.security.dependencies.acl import authenticate_active_user
from server.utils.enums import Tags
from server.utils.exceptions import handle_422_unprocessable_entity
from server.utils.helpers import create_tags


def create_oauth_applications_router() -> APIRouter:
    router = APIRouter(prefix="/apps", tags=create_tags([Tags.application]))

    @router.get("/health", response_model=MessageResponseSchema)
    async def health_check() -> MessageResponseSchema:
        return {"msg": "Applications Router is healthy"}

    @router.post("", response_model=ApplicationResponse)
    async def create_oauth_application(
        payload: ApplicationCreateSchema,
        user: TokenUser = Depends(authenticate_active_user),
        session: AsyncSession = Depends(get_database_session),
    ) -> ApplicationResponse:
        try:
            app = await create_new_application(session, payload, user)
            return app
        except Exception as e:
            raise e

    @router.get("", response_model=List[ApplicationResponse])
    async def read_oauth_application(
        user: TokenUser = Depends(authenticate_active_user),
        session: AsyncSession = Depends(get_database_session),
    ) -> ApplicationResponse:
        try:
            app = await read_applications(session, user.id)
            return app
        except Exception as e:
            raise e

    @router.patch("/{app_id}", response_model=ApplicationResponse)
    async def update_oauth_application(
        app_id: int,
        payload: ApplicationUpdateSchema,
        user: TokenUser = Depends(authenticate_active_user),
        session: AsyncSession = Depends(get_database_session),
    ) -> ApplicationResponse:
        try:
            if not payload.model_dump(exclude_unset=True):
                raise handle_422_unprocessable_entity("No data to update.")
            app = await update_application(session, app_id, user.id, payload)
            return app
        except Exception as e:
            raise e

    return router
