from typing import Any, TypeVar

from pydantic import BaseModel

from app.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)

SelectSchemaType = TypeVar("SelectSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
UpdateSchemaInternalType = TypeVar("UpdateSchemaInternalType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)

GetMultiResponseDict = dict[str, list[dict[str, Any]] | int]
GetMultiResponseModel = dict[str, list[SelectSchemaType] | int]
