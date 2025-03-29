from typing_extensions import Annotated

from pydantic import BaseModel, Field

from app.core import Overlay

from .mixins import TimestampSchema, UUIDSchema


class ProductSwatchBase(BaseModel):
    hex_color: Annotated[str, Field(..., description="Hex color code for the product", example="#151e24")]
    rgb_color: Annotated[list[int], Field(..., description="RGB color values", example=[21, 30, 36])]
    oklch_color: Annotated[list[float], Field(..., description="OKLCH color values", example=[0.229, 0.0175, 237.72])]
    gradient_start: Annotated[list[float], Field(..., description="Gradient start color in OKLCH", example=[0.229, 0.0175, 237.72])]
    gradient_end: Annotated[list[float], Field(..., description="Gradient end color in OKLCH", example=[0.229, 0.0175, 237.72])]
    overlay: Annotated[Overlay | None, Field(None, description="Optional SVG filter overlay for adding texture based on product type", example="chrome")]


class ProductSwatchCreate(ProductSwatchBase):

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


@partial_schema()
class ProductSwatchUpdate(ProductSwatchBase):

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


class ProductSwatchResponse(ProductSwatchBase, UUIDSchema, TimestampSchema):
    product_id: UUID

    class Config:
        from_attributes = True
