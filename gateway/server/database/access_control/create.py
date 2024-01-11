from server.models.database.acl import Permission, Role


async def create_admin_role() -> Role:
    role = Role(title="admin")
    return role


async def create_admin_permissions() -> list[Permission]:
    permissions = [
        Permission(object_name="all", action="create"),
        Permission(object_name="all", action="read"),
        Permission(object_name="all", action="update"),
        Permission(object_name="all", action="delete"),
    ]
    return permissions
