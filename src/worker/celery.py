import asyncio

from app import parsers
from dependency_injector.wiring import inject

from celery import Celery

celery_app = Celery("worker")
celery_app.config_from_object("worker.celeryconfig")

celery_app.conf.beat_schedule = {
    "scheduled_task": {"task": "worker.celery.celery_scheduled_task", "schedule": 30}
}


@celery_app.task
@inject
def celery_scheduled_task():
    parsers.init_container()
    asyncio.run(aggregate_data())


@inject
async def aggregate_data():
    await parsers.Spbgtu().worker()
