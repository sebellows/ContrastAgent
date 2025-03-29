from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UUIDMixin


if TYPE_CHECKING:
    from .user import User


class Tier(BaseEntity, UUIDMixin):
    __tablename__ = "tiers"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship(back_populates="tier", primaryjoin="Tier.id == User.tier_id")

    def __repr__(self) -> str:
        # return f"Tier(name={self.name})"
        self.to_repr(["name"])
