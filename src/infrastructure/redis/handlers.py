from infrastructure.redis.db import get_async_redis


async def change_period(period: int):
    async with get_async_redis() as r:
        pipe = r.pipeline()
        pipe.set("parsing_period", period)
        pipe.set("parsing_trigger", period, period)
        await pipe.execute()


async def create_parsing_period():
    async with get_async_redis() as r:
        pipe = r.pipeline()
        pipe.set("parsing_period", 86400)
        pipe.set("parsing_trigger", 86400, 86400)
        await pipe.execute()


async def set_parsing_trigger(period: int):
    async with get_async_redis() as r:
        pipe = r.pipeline()
        pipe.set("parsing_trigger", period, period)
        await pipe.execute()


async def get_parsing_period():
    async with get_async_redis() as r:
        parsing_period = await r.get("parsing_period")
        return parsing_period


async def get_parsing_trigger():
    async with get_async_redis() as r:
        parsing_trigger = await r.get("parsing_trigger")
        return bool(parsing_trigger)
