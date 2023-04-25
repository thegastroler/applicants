from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Callable
from typing import Optional, Type

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from infrastructure.sql import models


class ApplicantsRepository(ABC):
    model: Type

    @abstractmethod
    async def upload(self, data):
        ...


class SqlaApplicantsRepository(ApplicantsRepository):
    model = models.Applicants

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
