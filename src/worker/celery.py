import asyncio
import sys

from app import parsers
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from celery import Celery

celery_app = Celery("worker")
celery_app.config_from_object("worker.celeryconfig")

celery_app.conf.beat_schedule = {
    "scheduled_task": {"task": "worker.celery.celery_scheduled_task", "schedule": 60},
}


def init_container():
    container = SqlaRepositoriesContainer()
    container.wire(modules=[sys.modules[__name__]])


@celery_app.task
@inject
def truncate():
    init_container()
    asyncio.run(clear_table())


@celery_app.task
@inject
def celery_scheduled_task():
    truncate()
    asyncio.run(aggregate_data())


@inject
async def clear_table(use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])):
    await use_case.truncate()


@inject
async def aggregate_data():
    parsers.init_container()
    await parsers.Omgups().worker()
