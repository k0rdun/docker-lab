from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base
from postgresql import engine, get_session
from router import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield
    finally:
        await engine.dispose()


app = FastAPI(title='Books API', lifespan=lifespan)

app.include_router(books_router, prefix='/api/v1')


@app.get('/')
async def root():
    """Проверка доступности приложения."""
    return 'OK'


@app.get('/health')
async def health(session: AsyncSession = Depends(get_session)):
    """Проверка соединения с базой данных."""
    try:
        await session.execute(text('SELECT 1'))
    except (SQLAlchemyError, OSError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Database is unavailable',
        ) from None

    return {'status': 'ok', 'database': 'ok'}
