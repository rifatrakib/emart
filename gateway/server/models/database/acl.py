from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models.database import Base


class Group(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    title: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True, index=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="group_role",
        back_populates="groups",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="group_account",
        back_populates="groups",
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.title}")'


class Role(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    title: Mapped[str] = mapped_column(String(length=128), nullable=False, unique=True, index=True)

    groups: Mapped[list["Group"]] = relationship(
        "Group",
        secondary="group_role",
        back_populates="roles",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="role_permission",
        back_populates="roles",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="role_account",
        back_populates="roles",
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.title}")'


class Permission(Base):
    __table_args__ = (UniqueConstraint("object_name", "action"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    object_name: Mapped[str] = mapped_column(String(length=128), nullable=False)
    action: Mapped[str] = mapped_column(String(length=32), nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permission",
        back_populates="permissions",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="permission_account",
        back_populates="permissions",
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(object_name="{self.object_name}", action="{self.action}")'


class GroupRole(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey(column="group.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey(column="role.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(group_id="{self.group_id}", role_id="{self.role_id}")'


class RolePermission(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey(column="role.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey(column="permission.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(role_id="{self.role_id}", permission_id="{self.permission_id}")'


class GroupAccount(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey(column="group.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(group_id="{self.group_id}", account_id="{self.account_id}")'


class RoleAccount(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey(column="role.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(role_id="{self.role_id}", account_id="{self.account_id}")'


class PermissionAccount(Base):
    permission_id: Mapped[int] = mapped_column(
        ForeignKey(column="permission.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(permission_id="{self.permission_id}", account_id="{self.account_id}")'
