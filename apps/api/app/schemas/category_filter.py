from typing_extensions import Annotated

from fastapi_filter.fields import SearchField
from pydantic import BaseModel, Field


class CategoryFilter(BaseModel):
      application_method: Annotated[str | None, Field(default=None)]
      color_range: Annotated[str | None, Field(default=None)]
      name: Annotated[str | None, Field(default=None)]
      packaging_type: Annotated[str | None, Field(default=None)]
      product_type: Annotated[str | None, Field(default=None)]
      search: Annotated[SearchField | None, Field(default=None)]
      vendor_name: Annotated[str | None, Field(default=None)]
