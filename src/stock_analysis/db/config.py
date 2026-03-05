import os
from dotenv import load_dotenv
from pathlib import Path


def get_db_url(env: str) -> str:
    root = Path(__file__).resolve().parents[3]
    env_file = root / f".env.local.{env}"
    load_dotenv(env_file)

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
