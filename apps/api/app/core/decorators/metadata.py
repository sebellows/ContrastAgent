import inspect
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

def metadata(**kwargs):
    """
    Apply metadata to a function

    Example:
    --------
    >>> @metadata(_argcount=2)
    >>> def some_fn(a, b):
    >>>     return a * b
    >>> print(some_fn._argcount)
    2
    """
    def decorator(func):
        argspec = inspect.getfullargspec(func)

        # Statically add the number of parameters the function has. However, we
        # need to avoid `args`, because it's not possible to count them. The argspec
        # will list whether `*args` is present under the key `varargs`.
        setattr(func, '_argcount', None if argspec.varargs else len(argspec.args))

        if len(kwargs):
            for key, value in kwargs.items():
                setattr(func, key, value)

        return func
    return decorator
