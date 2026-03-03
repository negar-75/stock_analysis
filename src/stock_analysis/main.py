from fastapi import FastAPI
from stock_analysis.core.logging_config import setup_logging
from stock_analysis.api.routers.routers import api_routers
from dotenv import load_dotenv


setup_logging()

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="Stock Analysis")

    app.include_router(api_routers, prefix="/api/v1")
    return app


app = create_app()
