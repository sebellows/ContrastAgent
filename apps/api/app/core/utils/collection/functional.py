
from collections.abc import Callable
from functools import reduce


def apply_[T, T2](obj: T, func: Callable[[T], T2]):
    """
    Calls a function (`func`) on an object (`obj`), returning the result. Useful only in
    frequest functional programming standbys like `partial` and `compose`.

    Args:
    -----
    obj - Object to apply function to
    func - Function called with `obj`.

    Returns:
    --------
    Results of function applied to object..

    Example:
    --------
    >>> apply({ 'a': 1, 'b': 2 }, lambda obj: { k: 2 * v for k, v in obj.items() })
    { 'a': 2, 'b': 4 }
    """
    return func(obj)


def compose[**P, T](*funcs: list[Callable[P, T]]) -> Callable[P, T]:
    def callit(*args: P.args) -> T:
        return reduce(lambda acc, func: func(*acc), funcs, args)
    return callit

