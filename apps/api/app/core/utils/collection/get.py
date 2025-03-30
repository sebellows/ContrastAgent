from collections.abc import Hashable
from typing import Any, overload

from .assertions import is_namedtuple, is_numeric
from .path import to_paths

from .internal import UNSET, PathT


@overload
def get_[T, T2](obj: list[T], path: int, default: T2) -> T | T2: ...
@overload
def get_[T](obj: list[T], path: int, default: None = None) -> T | None: ...
@overload
def get_(obj: Any, path: PathT, default: Any = None) -> Any: ...
def get_(
    obj: Any,
    path: PathT,
    default: Any = None,
):
    """
    Get a nested value from an object based on the provided path.

    Args:
    -----
        obj: The object to retrieve the value from.
        path: The path to retrieve the value from. (Use when applying function in
            context where a named parameter is required, like using `functools.partial`.)
        default: The default value to return if the path does not exist.

    Examples:
    ---------
    >>> obj = {'a': 1, 'b': 2, 'c': {'d': {'e': 3}}}
    >>> get_(obj, 'c.d.e')
    3
    >>> get_(obj, 'c.d.f', default=4)
    4

    >>> getter = partial(get_, path='c.d.e')
    >>> value = getter(obj)
    3
    """
    value = obj

    # Create sentinel object from either UNSET, if default not set, or a dummy object,
    # which will help determine if should exit early.
    sentinel = default if default is UNSET else object()

    paths = to_paths(path)

    for key in paths:
        value = _get_value(value, key, default=default)

        if value is sentinel:
            # path does not exist, set obj to default and exit
            value = default
            break

    return value


def get_entry[T: (dict, list)](
    obj: T,
    path: Hashable | list[Hashable] | None = None,
    default=UNSET,
):
    value = obj
    entry: tuple[str, Any] | None = None

    # Create sentinel object from either UNSET, if default not set, or a dummy object,
    # which will help determine if should exit early.
    sentinel = default if default is UNSET else object()

    paths = to_paths(path)

    for key in paths:
        value = _get_value(value, key, default=default)
        entry = (key, value)

        if value is sentinel:
            # path does not exist, set obj to default and exit
            entry = (key, default)
            break

    return entry


def _get_value(obj: Any, key: str, default=UNSET):
    if isinstance(obj, dict):
        value = _get_from_dict(obj, key, default=default)
    elif is_namedtuple(obj):
        # Only allow `getattr` for namedtuple to avoid returning class
        # methods and/or attributes.
        value = getattr(obj, key) if hasattr(obj, key) else UNSET
    else:
        value = _get_from_item(obj, key, default=default)

    if value is UNSET:
        raise KeyError(f'Object "{repr(obj)}" does not have key "{key}"')

    return value


def _get_from_dict(obj: dict, key: int | str, default=UNSET):
    if (value := obj.get(key, UNSET)) is UNSET:
        value = default
        if not isinstance(key, int):
            value = obj.get(int(key), default)
    return value


def _get_from_item[T: (list, tuple)](obj: T, key: int | str, default=UNSET):
    if is_numeric(key) and (i := _get_index_key(key)) < len(obj):
        return obj[i]
    return default


def _get_index_key(key: int | str) -> int:
    if is_numeric:
        return key if isinstance(key, int) else int(key)
    raise ValueError(f"{key} is not a numeric type")
