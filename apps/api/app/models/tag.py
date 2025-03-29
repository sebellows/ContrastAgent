from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import product_tag_association
from .base import Base
from .mixins import UUIDMixin


if TYPE_CHECKING:
    from .product import Product


class Tag(Base, UUIDMixin):
    __tablename__ = "tags"

    value: Mapped[str] = mapped_column(unique=True, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(default="", nullable=True)

    # Relationships
    products = relationship("Product", secondary=product_tag_association, back_populates="tags")

    def __repr__(self) -> str:
        # return f"Tag(value={self.value})"
        self.to_repr(["value", "description"])
