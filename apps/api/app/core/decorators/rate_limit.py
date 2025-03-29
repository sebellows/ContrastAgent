from datetime import UTC, datetime
import hashlib
import time
from functools import wraps
from typing import Any, Callable

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..logger import logging


logger = logging.getLogger(__name__)

client: Redis | None = None


async def is_rate_limited(db: AsyncSession, user_id: int, path: str, limit: int, period: int) -> bool:
    if client is None:
        logger.error("Redis client is not initialized.")
        raise Exception("Redis client is not initialized.")

    current_timestamp = int(datetime.now(UTC).timestamp())
    window_start = current_timestamp - (current_timestamp % period)

    sanitized_path = path.strip("/").replace("/", "_")
    key = f"ratelimit:{user_id}:{sanitized_path}:{window_start}"

    try:
        current_count = await client.incr(key)
        if current_count == 1:
            await client.expire(key, period)

        if current_count > limit:
            return True

    except Exception as e:
        logger.exception(f"Error checking rate limit for user {user_id} on path {path}: {e}")
        raise e

    return False


def rate_limit(max_calls: int, period: int):
    """
    Rate limit by IP address after a set number of calls exceed a limit per minute.

    Source: [ArjanCodes](https://github.com/ArjanCodes/examples/2024/rate_limiting/rate_limiter_ip_only.py)

    Example
    -------
    ```python
    from fastapi import FastAPI, HTTPException, Request

    app = FastAPI()

    @app.get("/")
    @rate_limit(max_calls=5, period=60)
    async def read_root(request: Request):
        return { "message": "Hello, World!" }
    ```
    """
    def decorator(func: Callable[[Request], Any]) -> Callable[[Request], Any]:
        usage: dict[str, list[float]] = {}

        @wraps(func)
        async def wrapper(request: Request) -> Any:
            # get the client's IP address
            if not request.client:
                raise ValueError("Request has no client information")
            ip_address: str = request.client.host

            # create a unique identifier for the client
            unique_id: str = hashlib.sha256((ip_address).encode()).hexdigest()

            # update the timestamps
            now = time.time()
            if unique_id not in usage:
                usage[unique_id] = []
            timestamps = usage[unique_id]
            timestamps[:] = [t for t in timestamps if now - t < period]

            if len(timestamps) < max_calls:
                timestamps.append(now)
                return await func(request)

            # calculate the time to wait before the next request
            wait = period - (now - timestamps[0])
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Retry after {wait:.2f} seconds",
            )

        return wrapper

    return decorator
