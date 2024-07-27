from typing import ClassVar, Optional, Sequence

from pydantic import BaseModel, HttpUrl


class Vendor(BaseModel):
    id: str
    name: str
    url: HttpUrl
    platform: Optional[str]
    product_categories: Optional[Sequence[str]]
    product_ranges: Optional[Sequence[str]]
    table_name: ClassVar[str] = "vendor"


class VendorCreate(BaseModel):
    name: str
    url: HttpUrl
    platform: Optional[str]
    product_categories: Optional[Sequence[str]]
    product_ranges: Optional[Sequence[str]]


class VendorUpdate(BaseModel):
    name: str
    url: HttpUrl
    platform: Optional[str]
    product_categories: Optional[Sequence[str]]
    product_ranges: Optional[Sequence[str]]


class ResponseMessage(BaseModel):
    message: str


class VendorSearchResults(BaseModel):
    results: Sequence[Vendor]
