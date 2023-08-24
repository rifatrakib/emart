from fastapi import APIRouter
from server.utils.enums import Tags, Versions

router = APIRouter(prefix="/v1/auth", tags=[Tags.authentication, Versions.v1])


@router.get("/health")
async def health_check():
    return {"message": "Authentication router is up and running"}
