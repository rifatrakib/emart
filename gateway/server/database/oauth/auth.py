from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from server.database.accounts.read import read_account_by_access_token
from server.database.applications.read import read_application_by_client_id
from server.models.database.accounts import Account, Application


async def authenticate_oauth_user(
    session: AsyncSession,
    client_id: str,
    access_token: str,
) -> Tuple[Account, Application]:
    account = await read_account_by_access_token(session, access_token)
    application = await read_application_by_client_id(session, client_id)
    return account, application
