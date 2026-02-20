import os
from dotenv import load_dotenv
from pathlib import Path


def get_db_url(env: str) -> str:
    root = Path(__file__).resolve().parents[3]
    env_file = root / f".env.local.{env}"
    load_dotenv(env_file)

    return (
        f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:"
        f"{os.environ['POSTGRES_PASSWORD']}@"
        f"{os.environ['POSTGRES_HOST']}:"
        f"{os.environ['POSTGRES_PORT']}/"
        f"{os.environ['POSTGRES_DB']}"
    )
