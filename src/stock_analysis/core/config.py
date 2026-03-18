from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    redis_url: str
    secret_key: str
    algorithm: str
    rate_limit: int = 10
    rate_limit_window: int = 60
    finnhub_api_key: str
    openai_api_key:str

    model_config = SettingsConfigDict(case_sensitive=False)

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    return Settings(_env_file=env_file)
