from typing import Sequence, TYPE_CHECKING
from typing_extensions import Annotated

from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color

from app.core import ColorRange

from .mixins import TimestampSchema, UUIDSchema


# if TYPE_CHECKING:
#     from .product import ProductResponse

class ColorRangeBase(BaseModel):
    description: Annotated[str, Field(..., description="A description of what color values fall under this range", example="Turquoise consists of colors that are greenish-blue to bluish-green and encompasses colors that can be sub-categorized as cyan, teal, and azure, among others", default="")]


class ColorRangeResponse(ColorRangeBase, UUIDSchema, TimestampSchema):
    name: Annotated[ColorRange, Field(..., description="The name of the color range")]

    class Config:
        from_attributes = True
        use_enum_values = True


class ColorRangeCreate(ColorRangeBase):
    name: Annotated[ColorRange, Field(..., description="The name of the color range")]

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


@partial_schema()
class ColorRangeUpdate(ColorRangeBase):
    name: Annotated[ColorRange | None, Field(None, description="The name of the color range")]

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True

