from .internal import PathT
from .helpers import entries, properties


def pick(obj: dict, paths: list[str]):
    """
    Creates a dictionary composed only of the keys specified and their
    corresponding values.

    Args:
    -----
    obj - Dict to pull entries from.
    paths: - Variadic number of paths for values to retrieve from object.

    Returns:
    --------
    Dictionary composed only of keys specified and their corresponding values.

    Example:
    --------
    >>> pick({"a": 1, "b": 2, "c": {"d": {"e": 3}}}, "a", "b", "c.d.e")
    {"a": 1, "b": 2, "e": 3}
    """
    return entries(paths)(obj)


def pick_values(obj: dict, *paths: PathT):
    """
    Retrieve a list of values from a dict.

    Args:
    -----
    obj - Dict to pull values from.
    paths: - Variadic number of paths for values to retrieve from object.

    Returns:
    --------
    List of values from dict retreived using paths.

    Example:
    >>> pick_values({"a": 1, "b": 2, "c": {"d": {"e": 3}}}, "a", "b", "c.d.e")
    [1, 2, 3]
    """
    return properties(*paths)(obj)
