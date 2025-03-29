from typing_extensions import Annotated

from pydantic import BaseModel, Field

from .mixins import UUIDSchema, partial_schema


if TYPE_CHECKING:
    from .product_variant import ProductVariantResponse


class LocaleDetailsBase(BaseModel):
    name: Annotated[str | None, Field(..., description="The country name")]
    country_code: Annotated[str | None, Field(..., description="The ISO code for a country", example="US, GB, FR, etc.")]
    currency_code: Annotated[str | None, Field(..., description="The ISO currency code", example="USD or EUR")]
    currency_decimal_spaces: Annotated[int | None, Field(..., description="How many decimal spaces are used when formatting a price")]
    currency_symbol: Annotated[str | None, Field(..., description="The symbol used for representing a currency", example="'$', '€', etc.")]
    decimal_separator: Annotated[str | None, Field(..., description="The symbol used for denoting a formatted price as a decimal")]
    symbol_position: Annotated[str | None, Field(..., description="The position the currency symbol is placed at in a formatted price. Is either 'start' or 'end'", example="'$4.95' or '3.95F'")]


class LocaleDetailsResponse(LocaleDetailsBase, UUIDSchema):

    class Config:
        from_attributes = True


class LocaleDetailsCreate(LocaleDetailsBase):

    class Config:
        from_attributes = True
        validate_assignment = True


@partial_schema()
class LocaleDetailsUpdate(LocaleDetailsBase):

    class Config:
        from_attributes = True
        validate_assignment = True

