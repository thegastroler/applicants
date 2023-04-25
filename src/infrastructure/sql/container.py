from dependency_injector import containers, providers

from .config import AsyncDatabaseSettings
from .db import Database


class SqlAlchemyContainer(containers.DeclarativeContainer):
    settings = AsyncDatabaseSettings()
    db = providers.Singleton(Database, url=settings.url, debug=settings.debug)
    session_factory = providers.Factory(db.provided.session)
