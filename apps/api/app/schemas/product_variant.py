from typing_extensions import Annotated

from pydantic import BaseModel, Field

from app.core import Opacity, PackagingType, Viscosity

from .mixins import PaginatedResponseSchema, SoftDeletionSchema, TimestampSchema, UpdatedTimestampSchema, UUIDSchema


class ProductVariantBase(BaseModel):
    application_method: Annotated[ApplicationMethod | None, Field(None, description="Application technique that a product is specifically made for, like airbrushing or dry-brushing", example="Spray")]
    discontinued: Annotated[bool | None, Field(None, description="Whether the product is discontinued or not", example=False)]
    display_name: Annotated[str | None, Field(None, description="The product name as it should be displayed in the UI. Most useful for translations of product names, if available. Defaults to product name.", example="Leadbelcher")]
    image_url: Annotated[str | None, Field(description="URL to the product image", example="/app/resources/catalog/product/920x950/99209999051_sprayLeadbelcher.svg")]
    language_code: Annotated[str | None, Field(None, description="ISO language code", example="en")]
    locale_id: Annotated[UUID, Field(..., description="ID for the appropriate locale details")]
    marketing_name: Annotated[str | None, Field(..., description="Marketing name of the product variant", example="Leadbelcher")]
    opacity: Annotated[Opacity | None, Field(None, description="An assumed, not necessarily correct, description of the product's opaqueness", example="semi-opaque")]
    packaging: Annotated[PackagingType | None, Field(None, description="Product packaging type", example="Spray Can")]
    price: Annotated[int | None, Field(None, description="Price in smallest currency unit (e.g., cents)", example=475)]
    product_line: Annotated[str | None, Field(None, description="Product line name", example="Citadel")]
    product_url: Annotated[AnyUrl | None, Field(None, description="URL to the product page", example="https://www.warhammer.com/en-US/shop/Leadbelcher-Spray-US-2020")]
    sku: Annotated[str | None, Field(..., description="Stock keeping unit code", example="prod4540241-13209999111")]
    vendor_color_range: Annotated[list[str] | None, Field(default=[], description="Color ranges assigned by vendor", example=["Silver"])]
    vendor_product_id: Annotated[str | None, Field(None, description="Vendor's product ID", example="5ba77422-91cb-46dd-98d1-c108588cf6b6")]
    vendor_product_type: Annotated[list[str | None], Field(default=[], description="Product types assigned by vendor", example=["Spray"])]
    viscosity: Annotated[Viscosity | None, Field(None, description="An assumed, not necessarily correct, description of the product's viscosity.", example="high")]
    volume_ml: Annotated[int | None, Field(None, description="Product volume measured in milliliters (mL)", example=18)]
    volume_oz: Annotated[float | None, Field(description="Product volume measured in fluid ounces", example=0.6)]


class ProductVariantCreate(ProductVariantBase):

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


@partial_schema()
class ProductVariantUpdate(ProductVariantBase):

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


class ProductVariantDelete(BaseModel, SoftDeletionSchema):
    pass


class ProductVariantResponse(ProductVariantBase, UUIDSchema, TimestampSchema, SoftDeletionSchema):
    locale: LocaleDetailsResponse
    product_id: UUID
    vendor_color_range: list[str]
    vendor_product_type: list[str]

    class Config:
        from_attributes = True
        use_enum_values = True

