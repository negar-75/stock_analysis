from fastapi import FastAPI
from src.core.logging_config import setup_logging
from src.api.routers import price
from dotenv import load_dotenv
import uvicorn


setup_logging()

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="Stock Analysis")

    app.include_router(price.router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)