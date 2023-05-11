import sys
from typing import Dict, List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers, fastapi_users
from infrastructure.redis.handlers import change_period, create_parsing_period
from worker.celery import parse_data

from api.auth.auth import auth_backend
from api.auth.manager import create_user, get_user_manager
from api.auth.model import User
from api.auth.schemas import UserCreate, UserRead
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from app.schemas import ApplicantSchema

tags_metadata = [
    {
        "name": "force_parsing",
        "description": "Принудительно запустить парсинг вне очереди",
    },
    {
        "name": "change_parsing_period",
        "description": "Изменить период парсинга (_только для админа_)",
    },
    {
        "name": "search",
        "description": "Метод поиска данных (_только для админа_)",
    },
    {
        "name": "auth",
        "description": "Аутентификация",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

super_user = fastapi_users.current_user(superuser=True)

@app.on_event("startup")
async def startup_event():
    await create_user("abc@abc.abc", "admin", "123456", True)
    await create_parsing_period()
    parse_data.delay()


@app.get("/force_parsing", tags=["force_parsing"])
async def force_parsing(user: User = Depends(super_user)):
    parse_data.delay()
    return "Tasks delayed"


@app.get("/change_parsing_period", tags=["change_parsing_period"])
async def change_parsing_period(period: int, user: User = Depends(super_user)):
    await change_period(period)
    parse_data.delay()
    return "Parsing period changed"


@app.get("/search", tags=["search"])
@inject
async def get_data(
        snils: Optional[str] = None,
        code: Optional[str] = None,
        university: Optional[str] = None,
        use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])
    ) -> Dict[str, List[ApplicantSchema]]:
    if not any((snils, code, university)):
        return []
    result = await use_case.search(snils, code, university)
    return result

container = SqlaRepositoriesContainer()
container.wire(modules=[sys.modules[__name__]])
