import asyncio
import sys
from app.repository import SqlaRepositoriesContainer
from app import parsers
import uvicorn

if __name__ == "__main__":
    # container = SqlaRepositoriesContainer()
    # container.wire(modules=[sys.modules[__name__]])
    parsers.init_container()
    asyncio.run(parsers.Spbgeu().worker())
    # uvicorn.run(app, host="0.0.0.0", port=8000)