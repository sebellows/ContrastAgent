from collections.abc import Callable
from copy import copy, deepcopy
from functools import partial
from typing import Any

from .get import get_
from .internal import callit, getargcount
from .path import to_paths
from .transforms import to_iterator


def properties(*paths: list[str]) -> Callable[[object], list[Any]]:
    """
    Iterate over an object and returns a list of values based on the passed
    variadic number of paths.

    Args:
    -----
    paths - Variadic number of paths for values to retrieve from object.

    Returns:
    --------
    Function that returns values from object based on paths.

    Example:
    >>> getter = properties('a', 'b', 'c.d.e')
    >>> getter({'a': 1, 'b': 2, 'c': {'d': {'e': 3}}})
    {'a': 1, 'b': 2, 'e': 3}
    """
    getters = [partial(get_, path=path) for path in to_paths(paths)]

    return lambda obj: list([getter(obj) for getter in getters])


def property_(path: str) -> Callable[[object], Any]:
    return partial(get_, path=path)


def get__entry(obj: dict[str, Any], path: str) -> dict[str, Any]:
    """
    Helper function to get a single entry from an object based on the provided path.

    Args:
    -----
    obj - The object to retrieve the value from.
    path - The path to retrieve the value from.

    Returns:
    --------
    Dictionary with a single key-value pair where the key is the last part of the path
    and the value is the retrieved value from the object.

    Example:
    --------
    >>> get__entry({'a': 1, 'b': 2, 'c': {'d': {'e': 3}}}, 'c.d.e')
    {'e': 3}
    """
    # Retrieve the value using the get_ function
    value = get_(obj, path)

    # Extract the last part of the path to use as the key
    key = path.split('.')[-1] if '.' in path else path

    # Return a dictionary with the key and its corresponding value
    return {key: value}

def entries(*paths: list[str]) -> Callable[[object], dict[str, Any]]:
    """
    Iterate over an object and returns a dictionary composed of the entries found.

    Args:
    -----
    paths - Variadic number of paths for values to retrieve from object.

    Returns:
    --------
    Function that returns values from object based on paths.

    Example:
    --------
    >>> obj = {'a': 1, 'b': 2, 'c': {'d': {'e': 3}}}
    >>> getter = properties('a', 'b', 'c.d.e')
    >>> getter(obj)
    {'a': 1, 'b': 2, 'e': 3}
    """
    getters = [partial(get__entry, path=path) for path in to_paths(paths)]

    return lambda obj: dict([getter(obj) for getter in getters])



def clone(value, is_deep=False, customizer=None, key=None, _cloned=False):
    """
    Creates a clone of `value`. Supports deep clone and customizer callback.

    Args:
        value: Object to clone.

    Example:

        x = {"a": 1, "b": 2, "c": {"d": 3}}
        y = clone(x)
        y == y
        >>> True
        x is y
        >>> False
        x["c"] is y["c"]
        >>> True
        z = clone(x, is_deep=True)
        x['c'] is z['c']
        >>> False

    Returns:
        Cloned object.
    """
    clone_by = deepcopy if is_deep else copy
    result = None

    if callable(customizer) and not _cloned:
        argcount = getargcount(customizer, maxargs=4)
        cbk = partial(callit, customizer, argcount=argcount)
    elif _cloned:
        cbk = customizer
    else:
        cbk = None

    if cbk:
        result = cbk(value, key, value)

    if result is not None:
        return result

    if not _cloned:
        result = clone_by(value)
    else:
        result = value

    if cbk and not isinstance(value, str) and not isinstance(value, bytes):
        for key, subvalue in to_iterator(value):
            if is_deep:
                val = clone(subvalue, is_deep, cbk, key, _cloned=True)
            else:
                val = cbk(subvalue, key, value)

            if val is not None:
                result[key] = val

    return result
