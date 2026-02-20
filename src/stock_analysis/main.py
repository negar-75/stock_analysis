from fastapi import FastAPI
from stock_analysis.core.logging_config import setup_logging
from stock_analysis.api.routers import price
from dotenv import load_dotenv


setup_logging()

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="Stock Analysis")

    app.include_router(price.router)
    return app


app = create_app()
