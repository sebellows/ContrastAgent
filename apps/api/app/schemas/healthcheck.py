from typing_extensions import Annotated

from pydantic import BaseModel, Field

from .mixins import UUIDMixin


class HealthCheck(BaseModel, UUIDSchema):
    version: Annotated[str, Field(..., example="v1.1.12")]
    description: Annotated[str, Field(..., default="")]

    class Config:
        from_attributes = True
