import asyncio
from app.repository import SqlaRepositoriesContainer
from app import parsers
import uvicorn
from api.app import app, init_container

if __name__ == "__main__":
    # module = __name__
    # container = SqlaRepositoriesContainer()
    # container.wire(modules=[module])
    # asyncio.run(parsers.Ptsu().worker())
    init_container()
    uvicorn.run(app, host="0.0.0.0", port=8000)