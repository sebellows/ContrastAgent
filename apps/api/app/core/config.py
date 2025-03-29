from enum import Enum
from functools import lru_cache
import os

from fastapi.security import OAuth2PasswordBearer
from pydantic import field_validator
from pydantic_settings import BaseSettings
from starlette.config import Config as StarletteConfig

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, ".env")
config = StarletteConfig(env_path)


class EnvironmentOption(Enum):
    DEV = "development"
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class AppSettings(BaseSettings):
    APP_NAME: str = config('APP_NAME', default='color_agent')
    APP_TITLE: str = config('APP_TITLE', default='Color Agent')
    APP_DESCRIPTION: str = config('APP_DESCRIPTION', default='')
    APP_VERSION: str | None = config('APP_VERSION', default='0.1.0')
    APP_MAX_THREADS: int = config("APP_MAX_THREADS", default=100)
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)


class ApiSettings(BaseSettings):
    ENCODING = config('ENCODING', default='utf-8')
    API_PREFIX: str = config('API_V1_PREFIX', default='/api/v1')


class AdminUserSettings(BaseSettings):
    ADMIN_NAME: str = config("ADMIN_NAME", default="admin")
    ADMIN_EMAIL: str = config("ADMIN_EMAIL", default="admin@admin.com")
    ADMIN_USERNAME: str = config("ADMIN_USERNAME", default="admin")
    ADMIN_PASSWORD: str = config("ADMIN_PASSWORD", default="!Ch4ng3Th1sP4ssW0rd!")


class AuthSettings(BaseSettings):
    KEYCLOAK_URL: str = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
    KEYCLOAK_REALM: str | None = config("KEYCLOAK_REALM", default="coloragent-local")
    KEYCLOAK_CLIENT_ID: str | None = config('KEYCLOAK_CLIENT_ID', default=None)
    KEYCLOAK_CLIENT_SECRET: str | None = config('KEYCLOAK_CLIENT_SECRET', default=None)
    KEYCLOAK_ADMIN_USERNAME: str | None = config("KEYCLOAK_ADMIN_USERNAME", default=None)
    KEYCLOAK_ADMIN_PASSWORD: str | None = config("KEYCLOAK_ADMIN_USERNAME", default=None)

    OAUTH2_TOKEN_URL = OAuth2PasswordBearer(tokenUrl=f"{ApiSettings.API_PREFIX}/auth/token")

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7
    AUTH_EXCLUDE_PATHS: list[str] = [
        "/docs",
        "/redoc",
        "/openapi",
        "/auth/token",
        "/auth/token/refresh",
        "/register",
    ]


class LoggingSettings(BaseSettings):
    LOG_NAME: str = config('APP_NAME', default='app.logger')
    LOG_ACCESS_NAME: str = config("LOG_ACCESS_NAME", default="access.logger")
    LOG_LEVEL: str = config('LOG_LEVEL', default='DEBUG')
    LOG_HANDLER: str = 'RotatingFileHandler' # See docs [https://docs.python.org/3/library/logging.handlers.html]
    LOG_FILE_NAME: str = "app.log"
    LOG_FILE_MAX_BYTES: int = 10485760
    LOG_FILE_BACKUP_COUNT: int = 5
    LOG_FILE_ENCODING: str | None = None
    LOG_DIR_NAME: str = "logs"
    LOG_JSON_FORMAT = (
        "time: {time:YYYY-MM-DD HH:mm:ss Z} | "
        "level: {level} | "
        "request_id: {extra[request_id]} | "
        "user: {extra[user]} | "
        "user_host: {extra[user_host]} | "
        "user_agent: {extra[user_agent]} | "
        "url: {extra[path]} | "
        "method: {extra[method]} | "
        "request_data: {extra[request_data]} | "
        "response_data: {extra[response_data]} | "
        "response_time: {extra[response_time]} | "
        "response_code: {extra[response_code]} | "
        "message: {message} | "
        "exception: {exception}"
    )


class DatabaseSettings(BaseSettings):
    DB_CONNECTION: str = config("DB_CONNECTION", default="postgresql")
    DB_ADAPTOR: str = config("DB_ASYNC_ADAPTOR", default="postgresql+asyncpg://")
    DB_USER: str = config("DB_USER", default="postgres")
    DB_PASSWORD: str = config("DB_PASSWORD", default="postgres")
    DB_HOST: str = config("DB_HOST", default="localhost")
    DB_PORT: int = config("DB_PORT", default=5432)
    DB_NAME: str = config("DB_NAME", default="postgres")
    DB_ECHO_LOG: bool = bool(config("DB_ECHO_LOG", default=1))
    DB_URI: str = f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DB_URL = "sqlite:///:memory:"

    @field_validator("DB_URL", mode="before")
    @classmethod
    def prepare_db_url(cls, values: dict[str, str]) -> str:
        return '{0}+{1}://{2}:{3}@{4}:{5}/{6}'.format(
            values.get('DB_CONNECTION'),
            values.get('DB_ADAPTOR'),
            values.get('DB_USER'),
            values.get('DB_PASSWORD'),
            values.get('DB_HOST'),
            values.get('DB_PORT'),
            values.get('DB_NAME')
        )


class HttpSettings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[str] = ['*']


class ClientSideCacheSettings(BaseSettings):
    CLIENT_CACHE_MAX_AGE: int = config("CLIENT_CACHE_MAX_AGE", default=60)


class RedisCacheSettings(BaseSettings):
    REDIS_SERVICE_HOST: str = config('REDIS_SERVICE_HOST', default='localhost')
    REDIS_SERVICE_PORT: str = config('REDIS_SERVICE_PORT', default=6379)
    REDIS_SERVICE_URL: str = f"redis://{REDIS_SERVICE_HOST}:{REDIS_SERVICE_PORT}"
    # REDIS_CACHE_HOST: str = config("REDIS_CACHE_HOST", default=REDIS_SERVICE_HOST)
    # REDIS_CACHE_PORT: int = config("REDIS_CACHE_PORT", default=REDIS_SERVICE_PORT)


class RedisQueueSettings(BaseSettings):
    REDIS_QUEUE_HOST: str = config("REDIS_QUEUE_HOST", default=RedisCacheSettings.REDIS_SERVICE_HOST)
    REDIS_QUEUE_PORT: int = config("REDIS_QUEUE_PORT", default=RedisCacheSettings.REDIS_SERVICE_PORT)


class RateLimiterSettings(BaseSettings):
    RATE_LIMIT_HOST: str = config("RATE_LIMIT_HOST", default=RedisCacheSettings.REDIS_SERVICE_HOST)
    RATE_LIMIT_PORT: int = config("RATE_LIMIT_PORT", default=RedisCacheSettings.REDIS_SERVICE_PORT)
    RATE_LIMIT_URL: str = f"redis://{RATE_LIMIT_HOST}:{RATE_LIMIT_PORT}"
    RATE_LIMIT_MAX_CONNECTIONS: int = config("RATE_LIMIT_MAX_CONNECTIONS", default=10)
    RATE_LIMIT_PERIOD: int = config("RATE_LIMIT_PERIOD", default=3600)


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default=EnvironmentOption.LOCAL)


class GamesWorkshopSettings(BaseSettings):
    GW_ALGOLIA_API_KEY: str = config("GW_ALGOLIA_API_KEY", default="")
    GW_ALGOLIA_APP_ID: str = config("GW_ALGOLIA_APP_ID", default="")


class Settings(
    AppSettings,
    ApiSettings,
    AuthSettings,
    LoggingSettings,
    DatabaseSettings,
    HttpSettings,
    AdminUserSettings,
    ClientSideCacheSettings,
    RedisCacheSettings,
    RedisQueueSettings,
    RateLimiterSettings,
    EnvironmentSettings,
    GamesWorkshopSettings
):

    class SettingsConfig:
        env_file = ".env"


settings = Settings()


@lru_cache()
def get_settings():
    return Settings()

settings = Settings()
