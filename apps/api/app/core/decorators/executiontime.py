import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from ...logger import logger
from ..utils import printz

P = ParamSpec("P")
InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

def default_template(
    label: str,
    total_time: float,
    start_time: float | None = None,
    end_time: float | None = None,
):
    return "{0}: {1:.4f} seconds".format(label, total_time)

def executiontime(func: Callable[[InputT], OutputT]):
    @wraps(func)
    def decorator(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        printexecutiontime = kwargs.get('printexecutiontime', True)

        if not printexecutiontime:
            # exit early if we aren't going to log the execution time
            return result

        colors = kwargs.get('colors', ['PRIMARY', 'ACCENT'])
        label = kwargs.get('label', func.__name__)
        stdout = kwargs.get('stdout', None)
        use_logger: bool = kwargs.get('use_logger', True)
        template = kwargs.get('template', None)

        if template and not is_callable(template):
            printz("{_BOLD}{WARNING_BG}Warning:{BOLD_}{END} passed template parameter was not a function.")
            template = default_template

        msg = template(label, start_time, end_time, total_time)

        if use_logger:
            logger.log(msg)
        elif stdout:
            stdout.write(msg)
        elif kwargs.get('template', None) is None:
            printz("{_BOLD}{colors[0]}{l}:{BOLD_}{END} {colors[1]}{t:.4f} seconds{END}", l=label, t=total_time)
        else:
            print(msg)

        return result

    return decorator
