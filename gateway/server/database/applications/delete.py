from sqlalchemy.ext.asyncio import AsyncSession

from server.database.applications.read import read_application_by_id
from server.utils.exceptions import handle_404_not_found


async def delete_application(session: AsyncSession, app_id: int, user_id: int) -> None:
    app = await read_application_by_id(session, app_id, user_id)
    if not app:
        raise handle_404_not_found(msg="No OAuth application found")

    await session.delete(app)
    await session.commit()
