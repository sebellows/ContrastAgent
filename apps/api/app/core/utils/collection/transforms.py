from collections.abc import Iterable, Iterator, Mapping
from typing import Any

from .assertions import is_dict, is_iter, is_list, is_none, is_set, is_str, is_tuple


def to_iterator(obj: Any) -> Iterator:
    """
    Return iterative based on object type.
    """
    if isinstance(obj, Mapping):
        return obj.items()
    elif hasattr(obj, "items"):
        return iter(obj.items())
    elif isinstance(obj, Iterable):
        return enumerate(obj)
    else:
        return getattr(obj, "__dict__", {}).items()


def to_list(obj: Any):
    return obj if is_list(obj) else list(obj)


def to_set(obj: Any):
    return obj if is_set(obj) else set(obj)
#


def to_tuple(obj: Any):
    return obj if is_tuple(obj) else tuple(obj)
#


def to_dict(obj: Any, values: Iterable | None = None):
    if is_none(obj):
        return {}
    if is_dict(obj):
        return obj
    if is_iter(obj):
        if all(is_iter(item) and len(item) == 2 for item in obj):
            return dict(list(tuple(item) for item in obj))
        if is_list(obj) and all(is_str(item) for item in obj):
            return zip(obj, values) if values and len(values) else zip(obj, obj)
    raise ValueError(f"to_dict Error: object of type '{type(obj)}' cannot be converted to a dictionary")
#


def to_str(obj: Any):
    return obj if is_list(obj) else list(obj)
#
