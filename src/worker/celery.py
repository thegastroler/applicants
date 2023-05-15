import asyncio
from loguru import logger
import sys

from app import parsers
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.redis.handlers import (get_parsing_period,
                                           get_parsing_trigger,
                                           set_parsing_trigger)

from celery import Celery

celery_app = Celery("worker")
celery_app.config_from_object("worker.celeryconfig")

celery_app.conf.beat_schedule = {
    "scheduled_task": {"task": "worker.celery.celery_scheduled_task", "schedule": 5},
}


def init_container():
    container = SqlaRepositoriesContainer()
    container.wire(modules=[sys.modules[__name__]])


@celery_app.task
@inject
def parse_data():
    init_container()
    asyncio.run(aggregate_data())


@celery_app.task
@inject
def truncate():
    init_container()
    asyncio.run(clear_table())


@celery_app.task
def celery_scheduled_task():
    parsing_trigger = asyncio.run(get_parsing_trigger())
    if not parsing_trigger:
        parsing_period = asyncio.run(get_parsing_period())
        asyncio.run(set_parsing_trigger(parsing_period))
        asyncio.run(aggregate_data())


@inject
async def clear_table(use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])):
    await use_case.truncate()


@inject
async def aggregate_data():
    parsers.init_container()
    try:
        await parsers.Guz().worker()
        await parsers.Rgup().worker()
        await parsers.Mgotu().worker()
        await parsers.Spbgu().worker()
        await parsers.Pstu().worker()
        await parsers.Ugtu().worker()
        await parsers.Omgups().worker()
        await parsers.Spbgeu().worker()
        await parsers.Mggeu().worker()
        await parsers.Lesgaft().worker()
        await parsers.Ieup().worker()
        await parsers.Mhti().worker()
        await parsers.Spbutuie().worker()
        await parsers.Agtu().worker()
        await parsers.Rgsu().worker()
    except Exception as e:
        logger.info(e)
