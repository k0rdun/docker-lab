from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_books(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Book]:
        stmt = select(Book).order_by(Book.id).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_by_id(self, book_id: int) -> Book | None:
        stmt = select(Book).where(Book.id == book_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, *, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def update_by_id(self, book_id: int, data: dict) -> Book | None:
        book = await self.get_by_id(book_id)
        if book is None:
            return None

        for field, value in data.items():
            setattr(book, field, value)

        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_by_id(self, book_id: int) -> bool:
        book = await self.get_by_id(book_id)
        if book is None:
            return False

        await self.session.delete(book)
        await self.session.commit()
        return True
