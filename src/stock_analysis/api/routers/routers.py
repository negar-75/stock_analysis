from fastapi import FastAPI, APIRouter
from stock_analysis.api.routers import user, price


api_routers = APIRouter()

api_routers.include_router(price.router, prefix="/price", tags=["Prices"])
api_routers.include_router(user.router, prefix="/user", tags=["User"])
