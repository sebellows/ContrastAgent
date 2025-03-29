from typing import Sequence, TYPE_CHECKING
from typing_extensions import Annotated

from pydantic import BaseModel, Field

from .mixins import TimestampSchema, UpdatedTimestampSchema, UUIDSchema


# if typing.TYPE_CHECKING:
#     from .product import ProductResponse


class ProductTypeBase(BaseModel):
    description: Annotated[str, Field(description="A description of what color values fall under this range", example="Turquoise consists of colors that are greenish-blue to bluish-green and encompasses colors that can be sub-categorized as cyan, teal, and azure, among others", default="")]


class ProductTypeResponse(ProductTypeBase, TimestampSchema, UUIDSchema):
    name: Annotated[ProductType, Field(..., description="The name of the color range")]

    class Config:
        from_attributes = True
        use_enum_values = True


class ProductTypeCreate(ProductTypeBase):
    name: Annotated[ProductType, Field(..., description="The name of the color range")]

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


@partial_schema()
class ProductTypeUpdate(ProductTypeBase):
    name: Annotated[ProductType | None, Field(None, description="The name of the color range")]

    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True
