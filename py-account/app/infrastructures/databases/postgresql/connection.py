from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager

class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self, url: str):
        self._engine = create_async_engine(
            url,
            echo=False,  # Set to True for SQL logging
            future=True
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)  # type: ignore

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session.
        
        Usage:
            async with database.get_session() as session:
                # use session here
        """
        session = AsyncSession(self._engine, expire_on_commit=False)
        try:
            yield session
        finally:
            await session.close()
