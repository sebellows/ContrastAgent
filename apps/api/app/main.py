from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from anyio import to_thread
from arq.connections import RedisSettings

# import fastapi
from fastapi import APIRouter, FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_pagination import add_pagination

from app.api import router
from app.core import engine, settings
from app.core.config import (
    AppSettings,
    ClientSideCacheSettings,
    DatabaseSettings,
    EnvironmentOption,
    EnvironmentSettings,
    RedisCacheSettings,
    RedisQueueSettings,
    RedisRateLimiterSettings,
)
from app.core.middleware import LogMiddleware, CorrelationIdMiddleware
from app.core.services import setup_logging
from app.core.services.queue import close_redis_queue_pool, create_redis_queue_pool
from app.models import Base


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_tables_dev() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


setup_logging(json_logs=settings.LOG_JSON_FORMAT, log_level=settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Set number of tokens for the thread pool
    limiter = to_thread.current_default_thread_limiter()
    limiter.total_tokens = settings.APP_MAX_THREADS

    if isinstance(settings, DatabaseSettings):
        await create_tables()

    if isinstance(settings, RedisQueueSettings):
        await create_redis_queue_pool(
            RedisSettings(
                host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT
            )
        )

    yield

    if isinstance(settings, RedisQueueSettings):
        await close_redis_queue_pool()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    description=settings.APP_DESCRIPTION,
    contact={"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
)

# Add routers
app.include_router(router)

if (
    isinstance(settings, EnvironmentSettings)
    and settings.ENVIRONMENT != EnvironmentOption.PRODUCTION
):
    docs_router = APIRouter()

    # @docs_router.get("/docs", include_in_schema=False)
    # async def get_swagger_documentation() -> fastapi.responses.HTMLResponse:
    #     return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

    # @docs_router.get("/redoc", include_in_schema=False)
    # async def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
    #     return get_redoc_html(openapi_url="/openapi.json", title="docs")

    # @docs_router.get("/openapi.json", include_in_schema=False)
    # async def openapi() -> dict[str, Any]:
    #     out: dict = get_openapi(title=application.title, version=application.version, routes=application.routes)
    #     return out

    app.include_router(docs_router)


app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.DB_URI,
    engine_args={  # engine arguments example
        "echo": False,  # print all SQL statements
        "pool_pre_ping": True,
        "pool_size": 5,  # number of connections to keep open at a time
        "max_overflow": 10,  # number of connections to allow to be opened above pool_size
    },
)

app.add_middleware(LogMiddleware)
app.add_middleware(CorrelationIdMiddleware)

# Add pagination
add_pagination(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.DB_HOST, port=settings.DB_PORT, reload=True)
