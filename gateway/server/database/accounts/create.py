from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.database.access_control.create import create_admin_role
from server.models.database.accounts import Account, RefreshToken
from server.models.schemas.responses.auth import TokenCollectionSchema
from server.security.authentication.passlib import pwd_generator
from server.utils.enums import Provider
from server.utils.exceptions import handle_404_not_found


async def create_admin_account(session: AsyncSession) -> None:
    try:
        admin = Account(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            first_name=settings.ADMIN_FIRST_NAME,
            last_name=settings.ADMIN_LAST_NAME,
            is_verified=True,
            is_active=True,
            is_superuser=True,
        )

        admin.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        admin.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=admin.hash_salt,
                new_password=settings.ADMIN_PASSWORD,
            ),
        )
        admin.set_provider(provider=Provider.google)
        admin.roles.append(await create_admin_role())

        session.add(admin)
        await session.commit()
    except IntegrityError:
        await session.rollback()


async def create_new_account(session: AsyncSession, payload: dict[str, Any]) -> Account:
    try:
        account = Account(
            username=payload.username,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            is_active=True,
        )
        account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        account.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=account.hash_salt,
                new_password=payload.password,
            ),
        )

        session.add(account)
        await session.commit()
        await session.refresh(account)
        return account
    except IntegrityError:
        await session.rollback()
        raise handle_404_not_found("username or email already exists")


async def write_tokens(session: AsyncSession, account_id: int, tokens: TokenCollectionSchema):
    refresh_token = RefreshToken(
        refresh_token=tokens.refresh_token,
        access_token=tokens.access_token,
        account_id=account_id,
    )
    session.add(refresh_token)
    await session.commit()
