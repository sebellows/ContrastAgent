from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import ProductType as ProductTypeEnum

from .associations import product_product_type_association
from .base import Base
from .mixins import UUIDMixin


if TYPE_CHECKING:
    from .product import Product


class ProductType(Base, UUIDMixin):
    __tablename__ = "product_types"

    name: Mapped[str] = mapped_column(Enum(ProductTypeEnum), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(default="", nullable=True)

    # Relationships
    products = relationship("Product", secondary=product_product_type_association, back_populates="product_type")

    def __repr__(self) -> str:
        # return f"ProductType(name={self.name})"
        self.to_repr(["name", "description"])

