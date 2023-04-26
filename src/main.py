import requests
from bs4 import BeautifulSoup
import asyncio
from fastapi import Depends
from dependency_injector.wiring import Provide
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from app.parsers.rgsu import Rgsu
from app.parsers.mgotu import Mgotu
from app.parsers.rgup import Rgup


if __name__ == "__main__":
    module = __name__
    container = SqlaRepositoriesContainer()
    container.wire(modules=[module])
    # asyncio.run(Rgsu().worker())
    # asyncio.run(Mgotu().worker())
    asyncio.run(Rgup().worker())