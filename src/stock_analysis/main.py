"""
Stock Analysis FastAPI application entry point.

Creates and configures the FastAPI app with routers and logging.
"""

from fastapi import FastAPI
from stock_analysis.core.logging_config import setup_logging
from stock_analysis.api.routers.routers import ws_routers,rest_routers



setup_logging()




def create_app() -> FastAPI:
    app = FastAPI(title="Stock Analysis")

    app.include_router(rest_routers, prefix="/api/v1")
    app.include_router(ws_routers, prefix="/api/v1")
    return app


app = create_app()
