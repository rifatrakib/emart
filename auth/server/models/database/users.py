from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models.database import Base
from server.models.database.acl import Group, Permission, Role
from server.utils.enums import Gender, Provider


class Account(Base):
    username: Mapped[str] = mapped_column(String(length=64), nullable=True, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(length=256), nullable=True, unique=True, index=True)
    open_id: Mapped[str] = mapped_column(String(length=256), nullable=True, unique=True, index=True)
    _provider: Mapped[str] = mapped_column(String(length=16), nullable=True, index=True)
    _hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    _hash_salt: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user_account",
        uselist=False,
    )
    tokens: Mapped["RefreshToken"] = relationship(
        "RefreshToken",
        back_populates="account",
        uselist=True,
    )
    groups: Mapped[list[Group]] = relationship(
        Group,
        secondary="group_user",
        back_populates="users",
        order_by="Group.name",
    )
    roles: Mapped[list[Role]] = relationship(
        Role,
        secondary="role_user",
        back_populates="users",
        order_by="Role.name",
    )
    permissions: Mapped[list[Permission]] = relationship(
        Permission,
        secondary="permission_user",
        back_populates="users",
        order_by="Permission.object_name, Permission.action",
    )

    def __repr__(self) -> str:
        return f"<Account(username={self.username}, email={self.email}>"

    @property
    def provider(self) -> Provider:
        if self._provider == Provider.google:
            return Provider.google
        elif self._provider == Provider.facebook:
            return Provider.facebook
        elif self._provider == Provider.microsoft:
            return Provider.microsoft
        return None

    def set_provider(self, provider: str) -> None:
        self._provider = provider

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def set_hashed_password(self, hashed_password: str) -> None:
        self._hashed_password = hashed_password

    @property
    def hash_salt(self) -> str:
        return self._hash_salt

    def set_hash_salt(self, hash_salt: str) -> None:
        self._hash_salt = hash_salt


class Profile(Base):
    first_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(length=256), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    _birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    address: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    _gender: Mapped[str] = mapped_column(String(length=1), nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"), nullable=False, index=True)

    user_account: Mapped["Account"] = relationship(
        Account,
        cascade="all, delete",
        back_populates="user_profile",
        primaryjoin="Profile.account_id == Account.id",
        single_parent=True,
        lazy="joined",
        innerjoin=True,
    )

    def __repr__(self) -> str:
        return f"<Profile(first_name={self.first_name}, last_name={self.last_name}>"

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name_asian(self) -> str:
        return f"{self.last_name} {self.first_name}"

    @property
    def gender(self) -> Gender:
        if self._gender == Gender.male:
            return Gender.male
        elif self._gender == Gender.female:
            return Gender.female

    def set_gender(self, gender: Gender) -> None:
        self._gender = gender.value

    @property
    def birth_date(self) -> date:
        return self._birth_date

    def set_birth_date(self, birth_date: str) -> None:
        self._birth_date = birth_date


class RefreshToken(Base):
    refresh_token: Mapped[str] = mapped_column(String(length=1024), nullable=False, unique=True)
    access_token: Mapped[str] = mapped_column(String(length=1024), nullable=False, index=True, unique=True)

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False, index=True)

    account: Mapped[Account] = relationship(
        Account,
        back_populates="tokens",
        uselist=False,
        primaryjoin="RefreshToken.account_id == Account.id",
        lazy="joined",
        innerjoin=True,
    )

    def __repr__(self) -> str:
        return f"<RefreshToken(account_id={self.account_id}>"
