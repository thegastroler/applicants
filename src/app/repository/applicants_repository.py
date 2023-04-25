from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Callable
from typing import Optional, Type

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from infrastructure.sql import models


class ApplicantsRepository(ABC):
    model: Type

    @abstractmethod
    async def execute(self, rating_id: int):
        ...


class SqlaApplicantsRepository(ApplicantsRepository):
    # model = models.CoworkerReview

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def execute(self, rating_id: int) -> Optional[int]:
        async with self.session_factory() as session:
            print(rating_id)
            return
            # subquery = select(models.CoworkerProjectRating.coworker_review_id).filter_by(id=rating_id)
            # query_review = (
            #     update(models.CoworkerReview)
            #     .where(models.CoworkerReview.id.in_(subquery))
            #     .values(is_complete=False)
            #     .returning(models.CoworkerReview.id)
            # )
            # res_review = await session.execute(query_review)
            # await session.execute(
            #     update(models.CoworkerProjectRating).values(hr_comment=comment).filter_by(id=rating_id)
            # )
            # await session.commit()
            # return res_review.scalar_one_or_none()