from fastapi import HTTPException, status
from server.models.database.users import Account
from server.models.schemas.inc.auth import SignupRequestSchema
from server.security.authentication.password import pwd_generator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_account(session: AsyncSession, payload: SignupRequestSchema) -> Account:
    try:
        new_account = Account(username=payload.username, email=payload.email)
        new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        new_account.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=new_account.hash_salt,
                new_password=payload.password,
            )
        )

        session.add(instance=new_account)
        await session.commit()
        await session.refresh(instance=new_account)

        return new_account
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already exists",
        )
