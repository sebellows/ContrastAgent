from typing import Sequence, TYPE_CHECKING
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, Field

from .mixins import SoftDeletionSchema, TimestampSchema, UUIDSchema


if TYPE_CHECKING:
    from .product import ProductResponse


class TagBase(BaseModel):
    value: Annotated[str | None, Field(
        description="The a descriptor or label that helps refine categorization of a product.",
        example="'Terrain Effect', for describing an effect paint's application usage."
    )]
    description: Annotated[str, Field(..., description="A description, or additional context, rationalizing the tag.", example="This paint is best used for creating natural ground effects on bases or dioramas.", default="")]


class TagCreate(TagBase):

    class Config:
        from_attributes = True
        validate_assignment = True


@partial_schema()
class TagUpdate(TagBase):
    value: Annotated[str, Field(
        ...,
        description="The a descriptor or label that helps refine categorization of a product.",
        example="'Terrain Effect', for describing an effect paint's application usage."
    )]

    class Config:
        from_attributes = True
        validate_assignment = True


class TagResponse(TagBase, UUIDSchema, TimestampSchema):

    class Config:
        from_attributes = True

