from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.acl import Permission, Role
from server.models.schemas.requests.access_control import PermissionCreateSchema, RoleCreateSchema


async def create_admin_permissions() -> list[Permission]:
    permissions = [
        Permission(object_name="all", action="create"),
        Permission(object_name="all", action="read"),
        Permission(object_name="all", action="update"),
        Permission(object_name="all", action="delete"),
    ]
    return permissions


async def create_admin_role() -> Role:
    role = Role(title="admin")
    role.permissions.extend(await create_admin_permissions())
    return role


async def create_permission(session: AsyncSession, payload: PermissionCreateSchema) -> Permission:
    permission = Permission(**payload.model_dump())
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return permission


async def create_role(session: AsyncSession, payload: RoleCreateSchema) -> Role:
    role = Role(title=payload.title)
    role.permissions.extend([Permission(**p.model_dump()) for p in payload.permissions])
    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role
