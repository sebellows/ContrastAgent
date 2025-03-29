from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from .base import Base
from .mixins import UUIDMixin


if TYPE_CHECKING:
    from .product_variant import ProductVariant


symbol_position_choices = [
    ("start", "start"),
    ("end", "end"),
]

class LocaleDetails(Base, UUIDMixin):
    __tablename__ = "locale_details"
    __table_args__ = (
        UniqueConstraint('country_code', name='unique_locale')
    )

    name: Mapped[str] = mapped_column(nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=True)
    currency_symbol: Mapped[str] = mapped_column(String(5), nullable=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=True)
    currency_decimal_spaces: Mapped[int] = mapped_column(nullable=True)
    symbol_position: Mapped[str] = mapped_column(ChoiceType(symbol_position_choices), nullable=True)
    decimal_separator: Mapped[str] = mapped_column(nullable=True)

    # Relationships
    product_variants: Mapped[list["ProductVariant"]] = relationship("ProductVariant", back_populates="locale")

    def __repr__(self) -> str:
        # return f"LocaleDetails(name={self.name}, currency_code={self.currency_code})"
        return self.to_repr()
