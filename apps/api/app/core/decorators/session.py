from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, AyncQuery
# from sqlalchemy.orm import Query, Session

from .classproperty import classproperty


"""
Source: sqlalchemy-mixins (https://github.com/absent1706/sqlalchemy-mixins/)
"""

class NoSessionError(RuntimeError):
    pass

class SessionMixin:
    _session = None

    @classproperty
    async def session(cls):
        if cls._session is None:
            raise NoSessionError('Cant get session.')
        async with cls._session() as session:
            yield session

    @async_classproperty
    async def query(cls) -> AyncQuery:
        return await cls.session.query(cls)

    @classmethod
    def set_session(cls, session: AsyncSession):
        cls._session = session
