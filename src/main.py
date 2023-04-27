import asyncio
from app.repository import SqlaRepositoriesContainer
from app import parsers


if __name__ == "__main__":
    module = __name__
    container = SqlaRepositoriesContainer()
    container.wire(modules=[module])
    asyncio.run(parsers.Spbgtu().worker())