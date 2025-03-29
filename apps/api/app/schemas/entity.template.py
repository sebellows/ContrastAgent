from typing import Sequence, TYPE_CHECKING
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models import Model

from .mixins import PaginatedResponseSchema, SoftDeleteSchema, TimestampSchema, UpdatedTimestampSchema, UUIDSchema, partial_schema
from .mixins import SoftDeleteSchema, TimestampSchema, UpdatedTimestampSchema, UUIDSchema


if TYPE_CHECKING:
    # from .product import ProductResponse


class EntityBase(BaseModel):
    ...


class Entity(EntityBase, UUIDSchema):
    pass


class EntityResponse(EntityBase, UUIDSchema, SoftDeleteSchema, TimestampSchema):

    class Config:
        from_attributes = True


class EntityReadExternal(EntityResponse):
    pass
    # items: Annotated[list[Items], Field(default=[])]


class EntityCreate(EntityBase):
    pass


@partial_schema()
class EntityUpdate(EntityBase):
    pass


class EntityUpdateInternal(EntityUpdate, UpdatedTimestampSchema):
    pass


class EntityDelete(BaseModel, SoftDeleteSchema):
    pass


class EntityPaginatedResponse(BaseModel, PaginatedResponseSchema):
    pass
