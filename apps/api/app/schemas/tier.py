from pydantic import BaseModel, Field
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, Field

from .mixins import (
    CreatedTimestampSchema,
    SoftDeletionSchema,
    TimestampSchema,
    UUIDSchema
)


class TierBase(BaseModel):
    name: Annotated[str, Field(example="unlimited")]


class TierCreate(TierBase):

    class Config:
        from_attributes = True
        validate_assignment = True


class TierUpdate(TierBase):

    class Config:
        from_attributes = True
        validate_assignment = True


class TierDelete(BaseModel, SoftDeletionSchema):
    pass


class TierResponse(TierBase, TimestampSchema, UUIDSchema):

    class Config:
        from_attributes = True
