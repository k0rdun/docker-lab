from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from postgresql import get_session
from repository import BookRepository
from schemas import BookCreate, BookResponse


router = APIRouter(
    prefix='/books',
    tags=['books'],
)


@router.get('/', response_model=list[BookResponse])
async def list_books(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Получение списка книг с пагинацией."""
    repo = BookRepository(session)
    rows = await repo.list_books(limit=limit, offset=offset)
    return rows


@router.post(
    '/',
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    payload: BookCreate,
    session: AsyncSession = Depends(get_session),
):
    """Создание новой книги."""
    repo = BookRepository(session)
    row = await repo.create(**payload.model_dump())
    return row


@router.get('/{book_id}/', response_model=BookResponse)
async def get_book(
    book_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    """Получение книги по идентификатору."""
    repo = BookRepository(session)
    row = await repo.get_by_id(book_id)

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found',
        )

    return row


@router.put('/{book_id}/', response_model=BookResponse)
async def update_book(
    payload: BookCreate,
    book_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    """Обновление всех полей книги по идентификатору."""
    repo = BookRepository(session)
    row = await repo.update_by_id(book_id, payload.model_dump())

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found',
        )

    return row


@router.delete('/{book_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
) -> Response:
    """Удаление книги по идентификатору."""
    repo = BookRepository(session)
    deleted = await repo.delete_by_id(book_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found',
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
