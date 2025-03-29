from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")

class classproperty(property):
    """
    @property for @classmethod
    taken from http://stackoverflow.com/a/13624858

    @see https://discuss.python.org/t/add-a-supported-read-only-classproperty-decorator-in-the-stdlib/18090

    In Python, a classproperty is a decorator used to define a method that is bound to the class
    and not the instance of the class. It is similar to the @property decorator, but it operates
    on the class itself rather than instances. It is used to define methods that can access and
    modify class-level attributes.

    This will also support async classproperties in the same way it handles synchronous ones.

    When the async class property is accessed, it returns a coroutine that needs to be awaited.

    Example:
    --------
    >>> import asyncio
    >>>
    >>> class SomeClass:
    >>> _value = 10
    >>>
    >>> @classproperty
    >>> async def value(cls):
    >>>     await asyncio.sleep(1)
    >>>     return cls._value
    """

    def __init__(self, afget: Callable[[type[T]], R], *args, **kwargs) -> None:
        super().__init__(fget=None, *args, **kwargs)
        self._afget = afget

    def __get__(self, instance: T | None, cls: type[T]) -> R:
        return self._afget(cls)
