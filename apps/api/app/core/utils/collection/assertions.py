import datetime
import inspect
from collections import namedtuple
from collections.abc import Callable, Coroutine, Iterable, Mapping, Sequence
from types import FunctionType
from typing import Any, TypeIs

def is_dict(o: Any) -> TypeIs[dict]:
    return isinstance(o, dict)


def is_mapping(o: Any) -> TypeIs[Mapping]:
    return isinstance(o, Mapping)


def is_list(o: Any) -> TypeIs[list]:
    return isinstance(o, list)


def is_sequence(o: Any) -> TypeIs[Sequence]:
    return isinstance(o, Sequence)


def is_iter(o: Any) -> TypeIs[Iterable]:
    return isinstance(o, Iterable)


def is_str(o: Any) -> TypeIs[str]:
    return isinstance(o, str)


def is_set(o: Any) -> TypeIs[set]:
    return isinstance(o, set)


def is_tuple(o: Any) -> TypeIs[tuple]:
    return isinstance(o, tuple)


def is_none(o: Any) -> TypeIs[None]:
    return o is None


def is_error(o: Any) -> TypeIs[Exception]:
    return isinstance(o, Exception)


def is_date(obj: Any) -> bool:
    return isinstance(obj, datetime.date)
#


def is_datetime(obj: Any) -> bool:
    return isinstance(obj, datetime.datetime)
#


def is_function(o: Any) -> TypeIs[FunctionType]:
    return inspect.isfunction(o)


def is_async(o: Any) -> TypeIs[Coroutine]:
    """
    Example:
    --------
    >>> async def async_sum(lst: list[int]) -> int:
    >>>     await asyncio.sleep(1)
    >>>     return sum(lst)
    >>>
    >>> async def main():
    >>>     if (is_async(async_sum)):
    >>>         return await async_sum([2, 3, 4])
    >>>     return async_sum([8, 6, 7])
    >>>
    >>> if __name__ == 'main':
    >>>     total = await main()
    >>>     print(total)
    9
    """
    return inspect.iscoroutinefunction(o)


def is_empty(obj: Any) -> bool:
    return len(obj) == 0 if isinstance(obj, (dict, list, set, str, tuple)) else bool(obj)


def is_number(value: Any) -> bool:
    """
    Verify that a value is a
    number (integer or float). This function checks if the value is an instance of `int` or `float`.
    Example:
    --------
    >>> is_number(10)
    True
    >>> is_number(3.14)
    True
    >>> is_number('10')
    False
    >>> is_number('3.14')
    False
    >>> is_number(None)
    False
    >>> is_number('Steve')
    False
    """
    return isinstance(value, (int, float))


def is_numeric_str(value: Any) -> bool:
    """
    Verify that a value is an integer in string form.

    Example:
    --------
    >>> is_numeric_str('55')
    True
    >>> is_numeric_str(20)
    False
    """
    return isinstance(value, str) and value.isnumeric()


def is_numeric(value: Any) -> bool:
    """
    Verify that a value is either an integer or integer in string form.

    Example:
    --------
    >>> is_numeric(2)
    True
    >>> is_numeric('55')
    True
    >>> is_numeric('Steve')
    False
    """
    return isinstance(value, int) or is_numeric_str(value)


def is_namedtuple(obj: object) -> TypeIs[namedtuple]:
    """
    Verify that an object is an instance of a namedtuple.

    Example:
    --------
    >>> Point = collections.namedtuple('Point', ['x', 'y'])
    >>> p = Point(1, 2)

    >>> is_namedtuple(p)
    True
    >>> is_namedtuple(Point)
    True
    >>> is_namedtuple((1, 2))
    False
    >>> is_namedtuple([1, 2])
    False
    """
    cls = obj if inspect.isclass(obj) else type(obj)
    return (issubclass(cls, tuple) and
            isinstance(getattr(cls, '_fields', None), tuple) and
            all(isinstance(field, str) for field in cls._fields))


def eq(obj1: Any, obj2: Any) -> bool:
    return obj1 is obj2


def gt(obj1: Any, obj2: Any) -> bool:
    return obj1 > obj2
#


def gte(obj1: Any, obj2: Any) -> bool:
    return obj1 >= obj2
#


def lt(obj1: Any, obj2: Any) -> bool:
    return obj1 < obj2
#


def lte(obj1: Any, obj2: Any) -> bool:
    return obj1 <= obj2
#


def in_range(value: Any, start: Any = 0, end: Any = None) -> bool:
    if not is_number(value):
        return False
    if not is_number(start):
        start = 0
    if not is_number(end):
        end = start
        start = 0
    return start <= value < end


def equal_with(obj1: Any, obj2: Any, comparator: Callable[[Any, Any], bool] | None = None) -> bool:
    if callable(comparator):
        if (
            type(obj1) is type(obj2)
            and isinstance(obj1, (dict, list))
            and isinstance(obj2, (dict, list))
            and len(obj1) == len(obj2)
        ):
            o1 = obj1.items() if is_dict(obj1) else enumerate(obj1)
            equal = False

            for key, value in o1:
                if obj2[key]:
                    equal = equal_with(value, obj2[key], comparator)
                if not equal:
                    break
            return equal
        else:
            equal = comparator(obj1, obj2)
            return equal if isinstance(equal, bool) else False

    return eq(obj1, obj2)



# def eq_[T](obj: T) -> Callable[[T], bool]:
#     return partial(eq, obj)
#

