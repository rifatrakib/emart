import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from server.database.applications.read import read_application_by_id
from server.models.database.accounts import Application
from server.models.schemas.requests.applications import ApplicationUpdateSchema
from server.utils.exceptions import handle_404_not_found


async def update_application(
    session: AsyncSession,
    app_id: int,
    user_id: int,
    payload: ApplicationUpdateSchema,
) -> Application:
    app = await read_application_by_id(session, app_id, user_id)
    if not app:
        raise handle_404_not_found(msg="No OAuth application found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(app, key, value)

    await session.flush()
    await session.commit()
    await session.refresh(app)
    return app


async def regenerate_secrets(session: AsyncSession, app_id: int, user_id: int) -> Application:
    app = await read_application_by_id(session, app_id, user_id)
    if not app:
        raise handle_404_not_found(msg="No OAuth application found")

    app.client_id = secrets.token_hex(32)
    app.secret_key = secrets.token_hex(32)
    await session.flush()
    await session.commit()
    await session.refresh(app)
    return app
