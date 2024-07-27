from typing import ClassVar, Optional, Sequence

from pydantic import BaseModel, HttpUrl


class ProductType(BaseModel):
    id: str
    name: str
    slug: str
    product_count: Optional[int]
    table_name: ClassVar[str] = "product_type"


class ProductTypeCreate(BaseModel):
    name: str
    slug: str
    product_count: Optional[int]


class ProductTypeUpdate(BaseModel):
    name: str
    url: str
    product_count: Optional[int]
    platform: Optional[str]


class ResponseMessage(BaseModel):
    message: str


class ProductTypeSearchResults(BaseModel):
    results: Sequence[ProductType]
