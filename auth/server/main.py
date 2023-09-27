import subprocess
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse
from server.config.factory import settings
from server.database.profile.crud import create_admin_profile
from server.database.user.auth import create_admin_account, read_admin_account
from server.models.database import get_async_database_session
from server.models.schemas.inc.auth import SignupRequestSchema
from server.models.schemas.inc.profile import ProfileCreateSchema
from server.models.schemas.out.auth import TokenUser
from server.routes.account.v1 import router as account_router
from server.routes.auth.v1 import router as auth_router
from server.routes.profile.v1 import router as profile_router
from server.routes.sso.v1 import router as sso_router
from server.security.dependencies.acl import is_superuser
from server.utils.html import build_html
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router)
app.include_router(sso_router)
app.include_router(account_router)
app.include_router(profile_router)


def run_alembic_migration():
    subprocess.run("alembic upgrade head", shell=True)


@app.on_event("startup")
async def on_startup():
    run_alembic_migration()

    session: AsyncSession = get_async_database_session()

    try:
        await read_admin_account(session=session)
    except HTTPException:
        info = SignupRequestSchema(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
        )
        admin = await create_admin_account(session=session, payload=info)

        admin_info = ProfileCreateSchema(first_name=settings.ADMIN_FIRST_NAME, last_name=settings.ADMIN_LAST_NAME)
        await create_admin_profile(session=session, admin_account=admin, payload=admin_info)

    await session.close()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(
    request: Request,
    user: Union[TokenUser, None] = Depends(is_superuser),
):
    try:
        if user:
            return build_html({"request": request, "user": user.model_dump()}, "index.html")

        return build_html({"request": request, "user": None}, "index.html")
    except HTTPException as e:
        raise e


@app.get("/health")
async def health_check():
    return {"app_name": settings.APP_NAME}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_docs(user: Union[TokenUser, None] = Depends(is_superuser)):
    if user:
        return get_swagger_ui_html(openapi_url="/openapi.json", title=settings.APP_NAME + " - Swagger UI")

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response


@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi(user: Union[TokenUser, None] = Depends(is_superuser)):
    if user:
        return get_openapi(title=settings.APP_NAME, version="0.1.0", routes=app.routes)

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response
