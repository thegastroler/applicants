from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aioredis
from worker.celeryconfig import broker_url


@asynccontextmanager
async def get_async_redis() -> AsyncGenerator[aioredis.Redis, None]:
    redis: aioredis.Redis = await aioredis.from_url(broker_url)
    yield redis
    await redis.close()
