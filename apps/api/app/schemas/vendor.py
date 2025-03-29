from typing import Sequence
from typing_extensions import Annotated

from pydantic import BaseModel, Field, HttpUrl

from .mixins import PaginatedResponseSchema, SoftDeletionSchema, TimestampSchema, UUIDSchema


if TYPE_CHECKING:
    from .product_line import ProductLineCreate, ProductLineResponse


class VendorBase(BaseModel):
    description: Annotated[str, Field(..., description="Description of the vendor", default="" example="Games Workshop, founded in the UK in 1975...")]
    name: Annotated[str, Field(..., description="Name of the vendor", example="Vallejo")]
    platform: Annotated[str | None, Field(None, description="E-commerce platform used by the vendor", example="Shopify")]
    pdp_slug: Annotated[str | None, Field(None, description="Product detail page slug pattern", example="shop")]
    plp_slug: Annotated[str | None, Field(None, description="Product listing page slug pattern", example="plp")]
    slug: Annotated[str, Field(..., description="Slug for the vendor", example="games_workshop")]
    url: Annotated[
        HttpUrl | None,
        Field(..., pattern=r"^https://[^\s/$.?#].[^\s]*$", example="https://www.warhammer.com"),
    ]


class VendorCreate(VendorBase):
    product_lines: Annotated[list[ProductLineCreate], Field(default=[])]

    class Config:
        from_attributes = True
        validate_assignment = True


@partial_schema()
class VendorUpdate(VendorBase):

    class Config:
        from_attributes = True
        validate_assignment = True


class VendorDelete(BaseModel, SoftDeletionSchema):
    pass


class VendorResponse(VendorBase, SoftDeletionSchema, TimestampSchema, UUIDSchema):
    product_lines: list[ProductLineResponse]

    class Config:
        from_attributes = True


class VendorSimpleResponse(VendorBase, UUIDSchema):

    class Config:
        from_attributes = True


class VendorSearchResults(PaginatedResponseSchema[VendorResponse]):

    class Config:
        from_attributes = True
