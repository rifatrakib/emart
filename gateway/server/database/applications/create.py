import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.accounts import Application
from server.models.schemas.requests.applications import ApplicationCreateSchema
from server.models.schemas.responses.auth import TokenUser


async def create_new_application(
    session: AsyncSession,
    payload: ApplicationCreateSchema,
    user: TokenUser,
) -> Application:
    app = Application(
        name=payload.name,
        description=payload.description,
        callback_url=payload.callback_url,
        app_owner_id=user.id,
        client_id=secrets.token_hex(32),
        secret_key=secrets.token_hex(32),
    )

    session.add(app)
    await session.commit()
    await session.refresh(app)
    return app
