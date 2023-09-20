from server.models.database.users import Account, Profile
from server.models.schemas.inc.profile import ProfileCreateSchema, ProfileUpdateSchema
from server.utils.exceptions import raise_404_not_found, raise_409_conflict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_profile(
    session: AsyncSession,
    account_id: int,
    payload: ProfileCreateSchema,
) -> Profile:
    try:
        new_profile = Profile(
            first_name=payload.first_name,
            middle_name=payload.middle_name,
            last_name=payload.last_name,
            address=payload.address,
        )
        new_profile.set_gender(gender=payload.gender)
        new_profile.set_birth_date(birth_date=payload.birth_date)
        new_profile.account_id = account_id

        session.add(instance=new_profile)
        await session.commit()
        await session.refresh(instance=new_profile)

        return new_profile
    except IntegrityError:
        raise_409_conflict(message="profile already exists")


async def read_profile_by_username(session: AsyncSession, username: str) -> Profile:
    stmt = select(Profile).join(Account, Account.id == Profile.account_id).where(Account.username == username)
    query = await session.execute(stmt)
    user_profile = query.scalar()

    if not user_profile:
        raise_404_not_found(message=f"No profile found for the user {username}.")

    return user_profile


async def update_user_profile(
    session: AsyncSession,
    account_id: int,
    payload: ProfileUpdateSchema,
) -> Profile:
    select_stmt = select(Profile).where(Profile.account_id == account_id)
    query = await session.execute(statement=select_stmt)
    update_user = query.scalar()

    if not update_user:
        raise_404_not_found(message=f"No profile found for the user with account id {account_id}.")

    for field, update_value in payload.model_dump().items():
        if update_value:
            if field == "birth_date":
                update_user.set_birth_date(birth_date=update_value)
            if field == "gender":
                update_user.set_gender(gender=update_value)
            else:
                setattr(update_user, field, update_value)

    await session.flush()
    await session.commit()
    await session.refresh(instance=update_user)

    return update_user
