import os
from dotenv import load_dotenv

load_dotenv()


def get_db_url(db_evn_key: str) -> str:
    return (
        f"postgresql+psycopg2://{os.environ['DB_USER']}:"
        f"{os.environ['DB_PASSWORD']}@"
        f"{os.environ['DB_HOST']}:"
        f"{os.environ['DB_PORT']}/"
        f"{os.environ[db_evn_key]}"
    )
