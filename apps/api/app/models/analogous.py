from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db.mixins import id_column

from .associations import product_analogous_association
from .base import Base
from .mixins import UUIDMixin


if TYPE_CHECKING:
    from .product import Product


class Analogous(Base, UUIDMixin):
    __tablename__ = "analogous_tags"

    value: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        comment="A common color name or color classification with which this product's color may bear similarities."
    )
    description: Mapped[str] = mapped_column(default="")

    # Relationships
    products: Mapped[list["Product"]] = relationship("Product", secondary=product_analogous_association, back_populates="analogous")

    def __repr__(self) -> str:
        # return f"Analogous(value={self.value})"
        return self.to_repr(["value", "description"])
