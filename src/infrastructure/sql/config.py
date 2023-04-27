from pydantic import BaseSettings, BaseConfig


class AsyncDatabaseSettings(BaseSettings):
    host: str = "db:5432"
    user: str = "postgres"
    password: str = "postgres"
    db_name: str = "postgres"
    debug: bool = True

    class Config(BaseConfig):
        env_prefix = "postgres_"

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"
