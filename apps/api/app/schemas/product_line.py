from typing import Sequence
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, Field

from .mixins import PaginatedResponseSchema, SoftDeletionSchema, TimestampSchema, UUIDSchema


if TYPE_CHECKING:
    from .product import ProductCreate, ProductResponse


class ProductLineBase(BaseModel):
    description: Annotated[str | None, Field(None, description="Description of the product line", example="")]
    marketing_name: Annotated[str | None, Field(None, description="Marketing name of the product line", example="Citadel Paints")]
    name: Annotated[str, Field(..., description="Name of the product line", example="Citadel")]
    product_line_type: Annotated[str | None, Field(None, description="Type of the product line", example="Mixed")]
    slug: Annotated[str, Field(..., description="Color Agent slug for the product line", example="citadel")]
    vendor_slug: Annotated[str, Field(min_length=2, examples=["warpaints-fanatic", "game-color"])]


class ProductLineCreate(ProductLineBase):
    products: Annotated[list[ProductCreate], Field(default=[])]

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


@partial_schema()
class ProductLineUpdate(ProductLineBase):

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


class ProductLineDelete(BaseModel, SoftDeletionSchema):
    pass


class ProductLineResponse(ProductLineBase, TimestampSchema, SoftDeletionSchema, UUIDSchema):
    vendor_id: UUID
    products: list[ProductResponse]

    class Config:
        from_attributes = True
        use_enum_values = True
