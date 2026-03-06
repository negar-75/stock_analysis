from fastapi import APIRouter,Depends
from stock_analysis.api.routers import user,price
from stock_analysis.api.dependencies.rate_limiter import rate_limiter

api_routers = APIRouter(dependencies=[Depends(rate_limiter)])

api_routers.include_router(price.router, prefix="/price", tags=["Prices"])
api_routers.include_router(user.router, prefix="/user", tags=["User"])
