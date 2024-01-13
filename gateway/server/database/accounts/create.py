from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.database.access_control.create import create_admin_role
from server.models.database.accounts import Account
from server.models.schemas.requests.auth import SignupRequestSchema
from server.security.authentication.passlib import pwd_generator
from server.utils.enums import Provider


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


async def create_new_account(session: AsyncSession, payload: SignupRequestSchema) -> Account:
    try:
        account = Account(
            username=payload.username,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "username or email already exists"},
        )
