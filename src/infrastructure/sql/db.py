import logging
from asyncio import current_task
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy.ext import asyncio as async_sa
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
Base = declarative_base()

class Database:
    def __init__(self, url: str, debug: bool) -> None:
        self._engine = async_sa.create_async_engine(url, echo=debug)
        self._session_factory = async_sa.async_scoped_session(
            async_sa.async_sessionmaker(self._engine, class_=async_sa.AsyncSession, expire_on_commit=False),
            current_task,
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(
        self,
    ) -> Callable[..., AbstractAsyncContextManager[async_sa.AsyncSession]]:
        session: async_sa.AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as exc:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise exc
        finally:
            await session.close()
