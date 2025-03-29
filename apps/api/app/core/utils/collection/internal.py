"""
Helper functions for internal use within the collection-focused functions.
Most of these are adapted from Pydash (https://github.com/dgilland/pydash).
"""

import builtins
from collections.abc import Callable, Hashable
import inspect
import operator
from types import BuiltinFunctionType
from typing import Any, ParamSpec, TypeVar

#: Dictionary of builtins with keys as the builtin function and values as the string name.
BUILTINS = {value: key for key, value in builtins.__dict__.items() if isinstance(value, Hashable)}

#: Inspect signature parameter kinds that correspond to positional arguments.
POSITIONAL_PARAMETERS = (
    inspect.Parameter.VAR_POSITIONAL,
    inspect.Parameter.POSITIONAL_ONLY,
    inspect.Parameter.POSITIONAL_OR_KEYWORD,
)

def is_builtin(value: Any) -> bool:
    """
    Checks if `value` is a Python builtin function or method.

    Args:
    -----
    value: Value to check.

    Returns:
    --------
    Whether `value` is a Python builtin function or method.

    Example:
    --------
    >>> is_builtin(1)
    True
    >>> is_builtin(list)
    True
    >>> is_builtin("foo")
    False
    """
    try:
        return isinstance(value, BuiltinFunctionType) or value in BUILTINS
    except TypeError:
        return False


P = ParamSpec("P")
OutT = TypeVar("OutputT")

def from_decorated_argcount(func: Callable[P, OutT], maxargs: int | None = None) -> int:
    """Return argument count of decorated function."""
    argcount = func._argcount if hasattr(func, "_argcount") else None
    # Optimization feature where argcount of iteratee is known and properly
    # set by initiator. Can be None, as maxargs is not required.
    return maxargs if argcount is None else argcount


def getargcount(func: Callable[P, OutT], maxargs: int | None = None) -> int | None:
    """Return argument count of iteratee function."""

    argcount = from_decorated_argcount(func, maxargs)

    if isinstance(func, type) or is_builtin(func):
        # Only pass single argument to type iteratees or builtins.
        return 1 if argcount is None else argcount

    # VAR_POSITIONAL corresponds to *args so we only want to count parameters if there isn't a
    # catch-all for positional args.
    params = inspect.signature(func).parameters.values()

    is_positional = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params)

    if not is_positional:
        positional_params = [p for p in params if p.kind in POSITIONAL_PARAMETERS]
        argcount = len(positional_params)

    if argcount:
        return argcount
    
    # Signatures were added with these operator methods in Python 3.12.3 and 3.11.9 but their
    # instance objects are incorrectly reported as accepting varargs when they only accept a
    # single argument.
    if isinstance(func, (operator.itemgetter, operator.attrgetter, operator.methodcaller)):
        return 1

    argspec = inspect.getfullargspec(func)

    print('argcount: ', argcount, argspec)
    if argspec.varargs:
        return maxargs

    # If varargs are present, the iteratee is a variadic function,
    # so we cannot say there is a hard number for number of args.
    # If there are no varargs, we can safely assume the number of args
    # is the length of the argspec.
    argcount = len(argspec.args)

    return maxargs if argcount is None else argcount


def get_function_name():
    # get the frame object of the function
    frame = inspect.currentframe()
    return frame.f_code.co_name


def callit(func: Callable[[Any], Any], *args, **kwargs):
    """
    Inspect argspec of `iteratee` function and only pass the supported arguments
    when calling it.
    """
    maxargs = len(args)
    argcount = kwargs['argcount'] if 'argcount' in kwargs else getargcount(func, maxargs)
    argstop = min([maxargs, argcount])

    return func(*args[:argstop])

