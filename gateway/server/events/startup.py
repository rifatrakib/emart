import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI

from server.connections import get_async_database_session
from server.database.accounts.create import create_admin_account
from server.routes import create_health_check_router
from server.routes.access_control import create_access_control_router
from server.routes.accounts import create_accounts_router


def run_migration():
    subprocess.run(["alembic", "upgrade", "head"])


def add_routers(app: FastAPI):
    app.include_router(create_health_check_router(), prefix="/api")
    app.include_router(create_accounts_router(), prefix="/api")
    app.include_router(create_access_control_router(), prefix="/api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    add_routers(app)
    run_migration()
    await create_admin_account(get_async_database_session())
    yield
