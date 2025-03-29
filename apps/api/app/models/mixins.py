from datetime import datetime
from functools import partial
import logging
from os import getenv
from typing import Any, TypedDict, Unpack
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr, mapped_column, Mapped, MappedColumn

from app.core.utils import tz_aware_utc_now

from .fields import AwareDatetime

"""
Currently, there is no way to type hint the params of a library function, so this
will have to do. MappedColumnParams contains most of the most widely used parameters
for SQLAlchemy's `mapped_column` function.
"""
class MappedColumnParams(TypedDict, total=False):
    type_: Any  # SQLAlchemy type
    name: str
    nullable: bool
    primary_key: bool
    autoincrement: bool
    unique: bool
    index: bool
    default: Any
    server_default: Any
    comment: str
    foreign_keys: Any
    onupdate: Any
    insert_default: Any

"""
Setting the covariant to true in the following param spec will help for instances where
it could be not enough. By setting `covariant` to `True` Python can infer that if genertic
type "T" is a subtype of Generic "U". This makes it so that `Callable[T, ReturnType]` is a
subtype of `Callable[U, ReturnType]`.
"""
P = ParamSpec("P", bound=MappedColumnParams, covariant=True)
U = ParamSpec("U", bound=MappedColumnParams, covariant=True)

def mapped_column_mixin[T, **P](**defaultkwargs: P.kwargs) -> Callable[P, Mapped[T]]:
    """
    Returns a callback that will apply custom parameters to defaults on a MappedColumn definition.

    Example:
    --------
    >>> col_mixin = mapped_column_mixin(autoincrement=True, nullable=False, unique=True, primary_key=True)
    >>> id_column = col_mixin(name='id', index=True)
    >>> print(id_column.__dict__.keys())
    dict_keys(['autoincrement', 'nullable', 'unique', 'primary_key', 'name', 'index'])
    """
    return partial(mapped_column, **kwargs)


id_column = mapped_column_mixin[int](autoincrement=True, nullable=False, unique=True, primary_key=True)

class UUIDMixin:
    @declared_attr
    def id(cls) -> Final[MappedColumn[str]]:
        return mapped_column(
            primary_key=True,
            unique=True,
            default=uuid4,
            server_default=text("gen_random_uuid()")
        )

class TimestampMixin:
    @declared_attr
    def created_at(cls) -> Final[Mapped[datetime]]:
        return mapped_column(
            AwareDatetime,
            nullable=False,
            server_default=f"{tz_aware_utc_now()}"
        )

    @declared_attr
    def updated_at(cls) -> Final[Mapped[datetime]]:
        return mapped_column(
            AwareDatetime,
            nullable=True,
            default=None,
            onupdate=tz_aware_utc_now,
        )


class SoftDeleteMixin:
    @declared_attr
    def deleted_at(cls) -> Final[Mapped[datetime | None]]:
        return mapped_column(
            AwareDatetime,
            default=None,
            onupdate=tz_aware_utc_now
        )

    @declared_attr
    def is_deleted(cls) -> Final[Mapped[bool]]:
        return mapped_column(
            default=False,
            index=True
        )


class CrudTimestampMixin(TimestampMixin, SoftDeleteMixin):
    pass

