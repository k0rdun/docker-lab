from collections.abc import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import config


DATABASE_URL = URL.create(
    drivername='postgresql+asyncpg',
    username=config.postgres_user,
    password=config.postgres_password,
    host=config.postgres_host,
    port=config.postgres_port,
    database=config.postgres_db,
)

engine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение соединения с базой данных."""
    async with session_factory() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
