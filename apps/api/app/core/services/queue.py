from arq.connections import ArqRedis

pool: ArqRedis | None = None

"""
Arq Redis Queue

See https://threeofwands.com/the-inner-workings-of-arq/
"""

async def create_redis_queue_pool() -> None:
    queue.pool = await create_pool(RedisSettings(host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT))


async def close_redis_queue_pool() -> None:
    await queue.pool.aclose()  # type: ignore

async def enqueue_job(job_name: str, *args, **kwargs) -> None:
    """
    Enqueue a job in the Redis queue
    Automatically adds the correlation_id to the job
    """
    if pool is None:
        raise ValueError("Redis pool not initialized")

    """
    Optional parameters for `enque_job`:

    _job_id - if omitted, this gets generated randomly but you can supply your own. It's used to
        potentially stop a job executing multiple times concurrently.
    _queue_name - the name of a Redis sorted set to use as the job queue. You need to use this if you
        have several different services using the same Redis instance. Defaults to arq:queue.
    _defer_until, _defer_by - used to schedule jobs for later. If omitted, the job will be executed ASAP.
    _expires - skip executing the job if it hasn't run in this many seconds.
    _job_try - manually specify the job try. Job try is a variable Arq uses to track how many times
        the job has been (re-)run.
    """
    await pool.enqueue_job(job_name, *args, **kwargs)
