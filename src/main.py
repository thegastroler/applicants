import asyncio
import sys
from app.repository import SqlaRepositoriesContainer
from app import parsers
import uvicorn
from app.parsers import init_container

if __name__ == "__main__":
    # container = SqlaRepositoriesContainer()
    # container.wire(modules=[sys.modules[__name__]])
    init_container()
    asyncio.run(parsers.Omgups().worker())
    # uvicorn.run(app, host="0.0.0.0", port=8000)