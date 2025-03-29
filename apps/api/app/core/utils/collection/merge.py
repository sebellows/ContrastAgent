from collections import Counter
from collections.abc import Hashable, Sequence
from copy import deepcopy
from enum import Enum
from functools import partial, reduce
from typing import Any, Mapping, MutableMapping, overload

from .assertions import is_list, is_set, is_tuple

"""
Source: mergedeep <https://github.com/clarketm/mergedeep>
"""

class Strategy(Enum):
    # Replace `destination` item with one from `source` (default).
    REPLACE = 0
    # Combine `list`, `tuple`, `set`, or `Counter` types into one collection.
    ADDITIVE = 1
    # Alias to: `TYPESAFE_REPLACE`
    TYPESAFE = 2
    # Raise `TypeError` when `destination` and `source` types differ. Otherwise, perform a `REPLACE` merge.
    TYPESAFE_REPLACE = 3
    # Raise `TypeError` when `destination` and `source` types differ. Otherwise, perform a `ADDITIVE` merge.
    TYPESAFE_ADDITIVE = 4


# T = TypeVar("T")
# T2 = TypeVar("T2")
# T3 = TypeVar("T3")
# T4 = TypeVar("T4")
# T5 = TypeVar("T5")

@overload
def merge[T1, T2](
    obj: Mapping[Hashable, T1],
    *sources: Mapping[Hashable, T2]
) -> Mapping[Hashable, T1 | T2]: ...

@overload
def merge[T1, T2](obj: Sequence[T1], *sources: Sequence[T2]) -> list[T1 | T2]: ...


def merge(
    destination,
    *sources,
    strategy: Strategy = Strategy.ADDITIVE
) -> MutableMapping:
    """
    Merge. Merge deeply.

    Args:
    -----
    destination - The destination mapping
    sources - The source mappings
    strategy - The merge strategy
    """
    return reduce(partial(_deepmerge, strategy=strategy), sources, destination)


def _handle_merge_replace(destination: Any, source: Any, key: Hashable):
    if isinstance(destination[key], Counter) and isinstance(source[key], Counter):
        # Merge both destination and source `Counter` as if they were a standard dict.
        _deepmerge(destination[key], source[key])
        return
    # If a key exists in both objects and the values are `different`, the value
    # from the `source` object will be used.
    destination[key] = deepcopy(source[key])


def _handle_merge_additive(destination: Any, source: Any, key: Hashable):
    # Values are combined into one long collection if both destination and source are same type.
    if is_list(destination[key]) and is_list(source[key]):
        destination[key].extend(deepcopy(source[key]))
    elif is_set(destination[key]) and is_set(source[key]):
        destination[key].update(deepcopy(source[key]))
    elif is_tuple(destination[key]) and is_tuple(source[key]):
        destination[key] = destination[key] + deepcopy(source[key])
    elif isinstance(destination[key], Counter) and isinstance(source[key], Counter):
        destination[key].update(deepcopy(source[key]))
    else:
        _handle_merge[Strategy.REPLACE](destination, source, key)


def _handle_merge_typesafe(destination: Any, source: Any, key: Hashable, strategy: Strategy):
    # Raise a TypeError if the destination and source types differ.
    if type(destination[key]) is not type(source[key]):
        raise TypeError(
            f'destination type: {type(destination[key])} differs from source type: {type(source[key])} for key: "{key}"'
        )

    _handle_merge[strategy](destination, source, key)


_handle_merge = {
    Strategy.REPLACE: _handle_merge_replace,
    Strategy.ADDITIVE: _handle_merge_additive,
    Strategy.TYPESAFE: partial(_handle_merge_typesafe, strategy=Strategy.REPLACE),
    Strategy.TYPESAFE_REPLACE: partial(_handle_merge_typesafe, strategy=Strategy.REPLACE),
    Strategy.TYPESAFE_ADDITIVE: partial(_handle_merge_typesafe, strategy=Strategy.ADDITIVE),
}


def _is_recursive_merge(a: Any, b: Any):
    both_mapping = isinstance(a, Mapping) and isinstance(b, Mapping)
    both_counter = isinstance(a, Counter) and isinstance(b, Counter)
    return both_mapping and not both_counter


def _deepmerge(destination: Any, source: Any, strategy=Strategy.REPLACE):
    for key in source:
        if key in destination:
            if _is_recursive_merge(destination[key], source[key]):
                # If the key for both `destination` and `source` are both Mapping types (e.g. dict), then recurse.
                _deepmerge(destination[key], source[key], strategy)
            elif destination[key] is source[key]:
                # If a key exists in both objects and the values are `same`, the value from the `destination` object will be used.
                pass
            else:
                _handle_merge.get(strategy)(destination, source, key)
        else:
            # If the key exists only in `source`, the value from the `source` object will be used.
            destination[key] = deepcopy(source[key])
    return destination
