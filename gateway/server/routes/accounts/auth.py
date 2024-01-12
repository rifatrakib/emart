from fastapi import APIRouter

from server.utils.enums import Tags
from server.utils.helpers import create_tags


def create_auth_router():
    print("Creating auth router")
    router = APIRouter(prefix="/auth", tags=create_tags([Tags.authentication]))

    @router.get("/health")
    async def health_check():
        return {"message": "Accounts - Authentication"}

    return router
