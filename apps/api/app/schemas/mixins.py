from collections.abc import Sequence
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, create_model, field_serializer
from pydantic.fields import FieldInfo

from app.core.utils import tz_aware_utc_now


def partial_schema(optional_fields: list[str] = []):
    def wrapper(model: type[BaseModel]):
        def get_optional_fields():
            if len(optional_fields):
                return [(field_name, field_info) for field_name, field_info in model.model_fields.items() if field_name in optional_fields]
            return list(model.model_fields.items())

        def make_field_optional(field: FieldInfo, default: Any = None) -> tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = field.annotation | None
            return new.annotation, new

        return create_model(
            f"Partial{model.__name__}",
            __base__=model,
            __module__=model.__module__,
            **{field_name: make_field_optional(field_info) for field_name, field_info in get_optional_fields()},
        )
    return wrapper


class UUIDSchema:
    id: UUID = Annotated[Field(default_factory=uuid4)]


class TimestampSchema:
    created_at: datetime = Field(default_factory=lambda: tz_aware_utc_now.replace(tzinfo=None))
    updated_at: datetime = Field(default=None)

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime | None, _info: Any) -> str | None:
        if created_at is not None:
            return created_at.isoformat()

        return None

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime | None, _info: Any) -> str | None:
        if updated_at is not None:
            return updated_at.isoformat()

        return None


class CreatedTimestampSchema:
    created_at: datetime = Field(default_factory=lambda: tz_aware_utc_now.replace(txinfo=None))

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime | None, _info: Any) -> str | None:
        if created_at is not None:
            return created_at.isoformat()

        return None


class UpdatedTimestampSchema:
    updated_at: datetime = Field(default=None)

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime | None, _info: Any) -> str | None:
        if updated_at is not None:
            return updated_at.isoformat()

        return None


class SoftDeleteSchema:
    deleted_at: datetime | None = Field(default=None)
    is_deleted: bool = False

    @field_serializer("deleted_at")
    def serialize_dates(self, deleted_at: datetime | None, _info: Any) -> str | None:
        if deleted_at is not None:
            return deleted_at.isoformat()

        return None


class PaginatedResponseSchema[T]:
    page: Annotated[int, Field(description="The current paginated page", example=2)]
    total_pages: Annotated[int, Field(description="The total number of pages available", example=9)]
    total_items: Annotated[int, Field(description="The total number of records to paginate", example=9)]
    items_per_page: Annotated[int, Field(description="The total number of items per page", example=9)]
    results: Sequence[T]


class SearchResultsSchema[T]:
    results: Sequence[T]
