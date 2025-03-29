from collections.abc import Hashable
from typing import Any

from .assertions import is_namedtuple, is_numeric, is_numeric_str
from .path import to_paths

from .internal import UNDEFINED

def get_[T: (dict, list)](
    obj: T,
    path: Hashable | list[Hashable],
    default=UNDEFINED,
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

    # Create sentinel object from either UNDEFINED, if default not set, or a dummy object,
    # which will help determine if should exit early.
    sentinel = default if default is UNDEFINED else object()

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
    default=UNDEFINED,
):
    value = obj
    entry: tuple[str, Any] | None = None

    # Create sentinel object from either UNDEFINED, if default not set, or a dummy object,
    # which will help determine if should exit early.
    sentinel = default if default is UNDEFINED else object()

    paths = to_paths(path)

    for key in paths:
        value = _get_value(value, key, default=default)
        entry = (key, value)

        if value is sentinel:
            # path does not exist, set obj to default and exit
            entry = (key, default)
            break

    return entry


def _get_value[T: object](obj: T, key: Hashable, default=UNDEFINED):
    if isinstance(obj, dict):
        value = _get_from_dict(obj, key, default=default)
    elif is_namedtuple(obj):
        # Only allow `getattr` for namedtuple to avoid returning class
        # methods and/or attributes.
        value = getattr(obj, key, default)
    else:
        value = _get_from_item(obj, key, default=default)

    if value is UNDEFINED:
        raise KeyError(f'Object "{repr(obj)}" does not have key "{key}"')

    return value

def _get_from_dict[T: dict](obj: T, key: Hashable, default = UNDEFINED):
    if (value := obj.get(key, UNDEFINED)) is UNDEFINED:
        return obj.get(int(key), default) if is_numeric_str(key) else default
    return value

def _get_from_item[T: (list, tuple)](obj: T, key: Hashable, default=UNDEFINED):
    if is_numeric(key) and (i := _get_index_key(key)) < len(obj):
        return obj[i]
    return default

def _get_index_key(key: Hashable) -> int:
    if is_numeric:
        return int(key) if is_numeric_str(key) else key
    raise ValueError(f"{key} is not a numeric type")

