from collections.abc import Callable
from functools import partial
from typing import Any

from .helpers import clone
from .internal import PathT, callit, getargcount

from .get import get_
from .path import parse_key, to_paths


def _raise_if_restricted_key(key):
    # Prevent access to restricted keys for security reasons.
    if key in ["__globals__", "__builtins__"]:
        raise KeyError(f"access to restricted key {key!r} is not allowed")


def default_customizer(x):
    return x


def set_[T: (dict, list)](
    obj: T,
    path: PathT,
    updater: Callable[[Any], Any],
    customizer: Any = None,
):
    if not callable(updater):
        updater = default_customizer

    if customizer:
        if not callable(customizer):
            call_customizer = partial(callit, clone, customizer, argcount=1)
        else:
            argcount = getargcount(customizer)
            if argcount > 3:
                argcount = 3
            call_customizer = partial(callit, customizer, argcount=argcount)
    else:
        call_customizer = None

    default_type = dict if isinstance(obj, dict) else list
    paths = to_paths(path)
    last_key = paths[-1]

    target = obj

    for key in paths[:-1]:
        obj_val = get_(target, key, default=None)
        path_obj = None

        if call_customizer:
            path_obj = call_customizer(obj_val, key, target)

        if path_obj is None:
            path_obj = default_type

        _base_set(target, key, path_obj, allow_override=False)

        try:
            target = get_(target, key, default=None)
        except TypeError as exc:  # pragma: no cover
            try:
                target = target[int(key)]
                _failed = False
            except Exception:
                _failed = True

            if _failed:
                raise TypeError(
                    f"Unable to update object at index {key!r}. {exc}"
                ) from exc

    value = get_(target, last_key, default=None)
    _base_set(target, last_key, callit(updater, value))

    return obj


def _base_set(
    obj: dict | list, key: PathT, value: Any, allow_override: bool = True
) -> dict | list:
    """
    Set an object's `key` to `value`. If `obj` is a ``list`` and the `key` is the next available
    index position, append to list; otherwise, pad the list of ``None`` and then append to the list.

    Args:
    -----
    obj - Object to assign value to.
    key - Key or index to assign to.
    value - Value to assign.
    """
    if obj is None:
        return obj

    if isinstance(obj, dict) and key not in obj:
        obj[key] = value
        return obj

    if isinstance(obj, list):
        return update_list(obj, key, value)  # type: ignore

    if not hasattr(obj, key):  # type: ignore
        _raise_if_restricted_key(key)
        setattr(obj, key, value)  # type: ignore

    return obj


def update_list(obj: list, key: int, value: Any):
    key = parse_key(key)  # type: ignore

    if key < len(obj):
        obj[key] = value
    else:
        if key > len(obj):
            # Pad list object with None values up to the index key, so we can append the value
            # into the key index.
            obj[:] = (obj + [None] * key)[:key]
        obj.append(value)
    return obj
