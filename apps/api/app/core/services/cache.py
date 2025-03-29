from redis.async import ConnectionPool, Redis

pool: ConnectionPool | None = None
client: Redis | None = None

async def create_redis_cache_pool(self) -> None:
    cache.pool = redis.ConnectionPool.from_url(settings.REDIS_SERVICE_URL)
    cache.client = redis.Redis.from_pool(cache.pool)  # type: ignore


async def close_redis_cache_pool(self) -> None:
    await cache.client.aclose()  # type: ignore
