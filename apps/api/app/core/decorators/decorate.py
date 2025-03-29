import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
InT = TypeVar("InputT")
OutT = TypeVar("OutputT")

# type InputFn[**P, InT] = Callable[P, InT]
# type OutputFn[**P, InT] = Callable[P, OutT]
# type Transformer[**P, InT, OutT] = Callable[[InputFn[P, InT]], OutputFn[P, InT]]

def decorate(transform: Callable[[InT], OutT]) -> Callable[[Callable[P, InT]], Callable[P, OutT]]:
    def decorator(func: Callable[P, InT]) -> Callable[P, OutT]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> OutT:
            value = func(*args, **kwargs)
            return transform(value)

        return wrapper

    return decorator