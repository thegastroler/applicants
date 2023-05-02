import sys

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, FastAPI

from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from app.schemas import ApplicantSchema

app = FastAPI()


@app.get("/search")
@inject
async def get_data(snils: str, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> list[ApplicantSchema]:
    result = await use_case.search(snils)
    result = [ApplicantSchema.from_orm(i) for i in result]
    return result

container = SqlaRepositoriesContainer()
container.wire(modules=[sys.modules[__name__]])
