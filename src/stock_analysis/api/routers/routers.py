from fastapi import APIRouter, Depends
from stock_analysis.api.routers.rest import price, user, analysis
from stock_analysis.api.routers.websockets import market_ws
from stock_analysis.api.dependencies.rate_limiter import rate_limiter

rest_routers = APIRouter(dependencies=[Depends(rate_limiter)])
ws_routers = APIRouter()

rest_routers.include_router(price.router, prefix="/price", tags=["Prices"])
rest_routers.include_router(user.router, prefix="/user", tags=["User"])
rest_routers.include_router(analysis.router, tags=["Analysis"])
ws_routers.include_router(market_ws.router)
