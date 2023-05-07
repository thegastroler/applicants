from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Callable, Type

from infrastructure.sql import models
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


class ApplicantsRepository(ABC):
    model: Type

    @abstractmethod
    async def upload(self, data):
        ...

    @abstractmethod
    async def search(self, snils, code, university):
        ...

    @abstractmethod
    async def truncate(self):
        ...


class SqlaApplicantsRepository(ApplicantsRepository):
    model = models.Applicant

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def upload(self, data):
        async with self.session_factory() as session:
            await session.execute(insert(self.model)
                .values([
                    {
                        "snils": i.snils,
                        "code": i.code,
                        "university": i.university,
                        "score": i.score,
                        "origin": i.origin,
                        "position": i.position,
                    }
                    for i in data
                ]).on_conflict_do_nothing())
            await session.commit()

    async def search(self, snils, code, university):
        async with self.session_factory() as session:
            query = select(self.model)
            query = query.filter(self.model.snils == snils) if snils else query
            query = query.filter(self.model.code == code) if code else query
            query = query.filter(self.model.university == university) if university else query
            result = await session.execute(query)
            items = result.scalars()
            return items

    async def truncate(self) -> None:
        async with self.session_factory() as session:
            await session.execute(delete(self.model))
            await session.commit()
