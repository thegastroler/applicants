from app.repository.applicants_repository import (ApplicantsRepository,
                                                  SqlaApplicantsRepository)
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory
from infrastructure.sql.container import SqlAlchemyContainer


class SqlaRepositoriesContainer(DeclarativeContainer):
    applicants_repository: Factory[ApplicantsRepository] = Factory(
        SqlaApplicantsRepository, session_factory=SqlAlchemyContainer.session_factory.provided
    )
