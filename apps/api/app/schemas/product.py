from typing import Sequence
from typing_extensions import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .mixins import PaginatedResponseSchema, SoftDeletionSchema, TimestampSchema, UUIDSchema


if typing.TYPE_CHECKING:
    from .product_variant import ProductVariantCreate, ProductVariantResponse
    from .swatch import ProductSwatchCreate, ProductSwatchUpdate, ProductSwatchResponse


class ProductBase(BaseModel):
    name: Annotated[str, Field(..., description="Name of the product", example="Leadbelcher")]
    iscc_nbs_category: Annotated[str | None, Field(None, description="ISCC-NBS color category", example="Blackish Green")]
    color_range: Annotated[list[str], Field(default=[], description="Color range categories the product falls under", example=["Blue"])]
    product_type: Annotated[list[str], Field(default=[], description="Types of the product", example=["Acrylic", "Metallic"])]
    tags: Annotated[list[str], Field(default=[], description="Tags applied to the product", example=["Special Effect"])]
    analogous: Annotated[list[str], Field(default=[], description="Analogous color names", example=["Azure"])]


class ProductCreate(ProductBase):
    swatch: ProductSwatchCreate
    variants: Annotated[list[ProductVariantCreate], Field(default=[])]

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


@partial_schema()
class ProductUpdate(ProductBase):
    swatch: ProductSwatchUpdate | None = None

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


class ProductDelete(BaseModel, SoftDeletionSchema):
    pass


class ProductResponse(ProductBase, TimestampSchema, SoftDeletionSchema, UUIDSchema):
    product_line_id: UUID
    swatch: ProductSwatchResponse
    variants: list[ProductVariantResponse]

    class Config:
        from_attributes = True
        use_enum_values = True


class ProductSearchResults(
    BaseModel,
    PaginatedResponseSchema[ProductResponse]
):
    pass
