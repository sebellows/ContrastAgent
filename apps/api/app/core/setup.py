from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from .config import settings

DATABASE_URL = settings.DB_URI

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
