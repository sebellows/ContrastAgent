from collection.abc import Callable
from enum import StrEnum
from functools import wraps
import logging
import os
import threading
from time import sleep
from typing import Any, cast, ParamSpec, TypeVar

from arq import ArqRedis, create_pool
from arq.connections import RedisSettings
from executiontime import printexecutiontime, YELLOW, RED
from redis.async import ConnectionPool, Redis
import redis.asyncio as redis

from .config import settings
from .services import cache_provider as cache, queue_provider as queue


PREFIX = "."

class Stats(StrEnum):
    # Number of times the cached function was actually called.
    REFRESH = "Refresh"
    # Number of times that we executed the function in the current thread.
    WAIT = "Wait"
    # Number of time that we had to wait 1s for the data to be found in the cache.
    SLEEP = "Sleep"
    # Number of times the cached function raised an exception when called.
    FAILED = "Failed"
    # Number of times the functions result was not found in the cache.
    MISSED = "Missed"
    # Number of times the function's result was found in the cache.
    SUCCESS = "Success"
    # Number of times the default value was used because nothing is in the cache or the function failed.
    DEFAULT = "Default"

P = ParamSpec("P")
T = TypeVar("T", str, bytes)


def key_from_params(
    name: str,
    args: tuple[Any, ...] | None = None,
    kwargs: dict[str, Any] | None = None,
    params: list[int | str] = []
) -> str:
    """
    Create a key from the function's name and its parameters values
    """

    values = []

    if len(params):
        for param in params:
            if isinstance(param, int) and len(args) >= param:
                values.append(str(args[param]))
            elif isinstance(param, str) and param in kwargs:
                values.append(f"{str(param)}='{str(kwargs[param])}'")
    else:
        if len(args):
            values.extend([str(arg) for arg in args])
        if len(kwargs):
            values.extend([f"{str(key)}='{str(value)}'" for key, value in kwargs.items()])

    return f"{name}({",".join([str(value) for value in values])})"


class RedisCache:
    """
    Args:
    -----

    decode
        Decode the data stored in the cache as byte string. For example, it should not be done if you actually want to cache
        byte strings. [Default: True]
    enabled
        When False it allows to programmatically disable the cache. It can be useful for unit tests. [Default: True]
    """

    client: Redis
    queue: ArqRedis

    def __init__(
        self,
        decode: bool = True,
        enabled: bool = True,
    ):
        self.enabled = enabled
        if self.enabled:
            pool: ConnectionPool = redis.ConnectionPool.from_url(settings.REDIS_SERVICE_URL)
            self.client = redis.Redis.from_pool(pool)  # type: ignore
            self.queue = await create_pool(RedisSettings(host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT))

    def cache(
        self,
        refresh: int,
        expire: int,
        default: T,
        retry: int | None = None,
        wait: bool = False,
        params: list[int | str] = [],
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """
        Having the decorator provided by a class allows to have some context to improve performances.

        Params
        ------

        refresh
            The amount of seconds before it would be a good idea to refresh the cached value.
        expire
            How many seconds that the value in the cache is still considered good enough to be sent back to the caller.
        retry
            While a value is being refreshed, we want to avoid to refresh it in parallel. But if it is taking too long, after
            the number of seconds provided here, we may want to try our luck again. If not specified, we will take the refresh value.
        default
            If we do not have the value in the cache and we do not want to wait, what shall we send back to the caller?
            It has to be serializable because it will also be stored in the cache. ['']
        wait
            If the value is not in the cache, do we wait for the return of the function? [False]
        """

        logger = logging.getLogger(__name__)

        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            """
            The decorator itself returns a wrapper function that will replace the original one.
            """

            @executiontime
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                """
                This wrapper calculates and displays the execution time of the function.
                """

                @executiontime()
                def refresh_value(key: str) -> T:
                    """
                    This gets the value provided by the function and stores it in local Redis database
                    """
                    try:
                        # Get some stats
                        self.client.incr(Stats.REFRESH)
                        # Execute function to fetch value to cache
                        new_value = func(*args, **kwargs)
                    # pylint: disable=broad-except
                    # It is normal to catch all exception because we do not know what function is decorated.
                    except Exception as exception_in_thread:
                        # Get some stats
                        self.client.incr(Stats.FAILED)
                        # Log the error. It's not critical because maybe next time it will work.
                        logger.error(
                            "Error in Thread execution to update the Redis cache on key %s\n%s",
                            key,
                            exception_in_thread,
                        )
                        # Since we have no value, let's use the default
                        self.client.incr(Stats.DEFAULT)
                        new_value = default

                    # Store value in cache with expiration time
                    self.client.set(key, new_value, ex=expire)
                    # Set refresh key with refresh time
                    self.client.set(PREFIX + key, 1, ex=refresh)
                    return new_value

                def refresh_value_in_thread(key: str) -> None:
                    """
                    Run the refresh value in a separate thread
                    """
                    thread = threading.Thread(target=refresh_value, args=(key,))
                    thread.start()

                # If the cache is disabled, directly call the function
                if not self.enabled:
                    return function(*args, **kwargs)

                # Lets create a key from the function's name and its parameters values
                key = key_from_params(name=function.__name__, args=args, kwargs=kwargs, params=params)

                # Get the value from the cache.
                # If it is not there we will get None.
                cached_value = cast(T, self.client.get(key))

                # Time to update stats counters
                self.client.incr(Stats.MISSED if cached_value is None else Stats.SUCCESS)

                # If the refresh key is gone, it is time to refresh the value.
                if self.client.set(PREFIX + key, 1, ex=retry if retry else refresh, nx=True):

                    # If we found a value in the cash, we will not wait for the refresh
                    if cached_value or not wait:
                        # We just update the cache in another thread.
                        refresh_value_in_thread(key)
                    else:
                        # Here we will wait, let's count it
                        self.client.incr(Stats.WAIT)
                        # We update the cash and return the value.
                        cached_value = refresh_value(key)

                # We may still have decided to wait but another process is already getting the cache updated.
                if cached_value is None and wait:
                    # Let's wait, but this is dangerous if we never get the value in the cache.
                    # We will stop if we lose the refresh key indicating that the refreshing timed out.
                    while cached_value is None and self.client.get(PREFIX + key):
                        # Let's count how many times we wait 1s
                        self.client.incr(Stats.SLEEP)
                        sleep(1)
                        cached_value = cast(T, self.client.get(key))

                # If the cache was empty, we have None in the cached_value.
                if cached_value is None:
                    # We are going to return the default value
                    self.client.incr(Stats.DEFAULT)
                    cached_value = default

                # Return whatever value we have at this point.
                return cached_value

            # If we want to bypass the cache at runtime, we need a reference to the decorated function
            wrapper.func = func  # type: ignore

            return wrapper

        return decorator

    def get_stats(self, delete: bool = False) -> dict[str, Any]:
        """
        Get the stats stored by RedisCache. See the list and definition at the top of this file.
        If delete is set to True we delete the stats from Redis after read.
        From Redis 6.2, it is possible to GETDEL, making sure that we do not lose some data between
        the 'get' and the 'delete'. But it is not available in the Redis (v3.5.3) python interface yet.
        """
        stats = { stat.value: self.client.get(stat) for stat in Stats}
        if delete:
            for stat in STATS:
                self.client.delete(stat)
        return stats

    async def close(self):
        await self.client.aclose()  # type: ignore
        await self.queue.aclose()  # type: ignore
