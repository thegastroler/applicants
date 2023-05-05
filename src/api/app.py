import sys
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, FastAPI

from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from app.schemas import ApplicantSchema

app = FastAPI()


@app.get("/search")
@inject
async def get_data(
        snils: Optional[str] = None,
        code: Optional[str] = None,
        university: Optional[str] = None,
        use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])
    ) -> list[ApplicantSchema]:
    if not any((snils, code, university)):
        return []
    result = await use_case.search(snils, code, university)
    result = [ApplicantSchema.from_orm(i) for i in result]
    return result

container = SqlaRepositoriesContainer()
container.wire(modules=[sys.modules[__name__]])
