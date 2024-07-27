from typing import ClassVar, Optional, Sequence

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    product_type: list[str]
    color_range: str
    color_value: str
    currency_code: str
    description: str
    gradient_start: str
    gradient_end: str
    price: str
    product_id: str
    slug: str
    vendor: str
    table_name: ClassVar[str] = "products"


class ProductCreate(BaseModel):
    name: str
    product_type: list[str]
    color_range: str
    color_value: str
    currency_code: str
    description: str
    gradient_start: str
    gradient_end: str
    price: str
    product_id: str
    slug: str
    vendor: str


class ProductUpdate(BaseModel):
    id: str
    name: str
    product_type: list[str]
    color_range: str
    color_value: str
    currency_code: str
    description: str
    gradient_start: str
    gradient_end: str
    price: str
    product_id: str
    slug: str
    vendor: str


class ProductSearchResults(BaseModel):
    results: Sequence[Product]
