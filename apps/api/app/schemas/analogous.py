from typing import Sequence, TYPE_CHECKING
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models import Analogous

from .mixins import TimestampSchema, UUIDSchema

if TYPE_CHECKING:
    from .product import ProductResponse


class AnalogousBase(BaseModel):
    value: Annotated[str, Field(
        ...,
        description="A common color name or color classification with which this product's color may bear similarities.",
        example="Azure"
    )]
    description: Annotated[str | None, Field(None, description="A description, or additional context, rationalizing the analogous label.", example="Azure is a color between cyan and blue, similar to this product's color.")]


class AnalogousCreate(AnalogousBase):

    class Config:
        from_attributes = True
        validate_assignment = True


@partial_schema()
class AnalogousUpdate(AnalogousBase):

    class Config:
        from_attributes = True
        validate_assignment = True


class AnalogousResponse(AnalogousBase, UUIDSchema, TimestampSchema):

    class Config:
        from_attributes = True

