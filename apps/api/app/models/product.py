from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import product_color_range_association, product_product_type_association, product_tag_association, product_analogous_association
from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


if TYPE_CHECKING:
    from .analogous import Analogous
    from .color_range import ColorRange
    from .product_line import ProductLine
    from .product_type import ProductType
    from .product_swatch import ProductSwatch
    from .product_variant import ProductVariant
    from .tag import Tag
    from .vendor import Vendor


class Product(Base, UUIDMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "products"

    product_line_id: Mapped[UUID] = mapped_column(ForeignKey('product_lines.id'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(default="")
    iscc_nbs_category: Mapped[str] = mapped_column(nullable=False)

    # Relationships
    product_line: Mapped["ProductLine"] = relationship("ProductLine", back_populates="products")
    swatch: Mapped["ProductSwatch"] = relationship("ProductSwatch", back_populates="product", uselist=False, cascade="all, delete-orphan")
    variants: Mapped[list["ProductVariant"]] = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")

    # Many-to-many relationships
    analogous = relationship("Analogous", secondary=product_analogous_association, back_populates="products")
    color_range = relationship("ColorRange", secondary=product_color_range_association, back_populates="products")
    product_type = relationship("ProductType", secondary=product_product_type_association, back_populates="products")
    tags = relationship("Tag", secondary=product_tag_association, back_populates="products")

    def __repr__(self) -> str:
        # return f"Product(name={self.name}, vendor_id={self.vendor_id})"
        return self.to_repr(["name", "description", "iscc_nbs_category", "product_line_id"])
