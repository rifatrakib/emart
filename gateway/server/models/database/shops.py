from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models.database import Base


class Shop(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(length=256), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    country: Mapped[str] = mapped_column(String(length=64), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(length=256), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(length=32), nullable=False)
    links: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

    merchant_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    merchant: Mapped["Account"] = relationship(
        "Account",
        back_populates="shops",
        uselist=False,
        innerjoin=True,
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.name}")'
