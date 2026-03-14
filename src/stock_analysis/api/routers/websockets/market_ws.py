from fastapi import APIRouter, WebSocket
from stock_analysis.services.price.realtime_service import RealTimeMarketSerive

router = APIRouter()


@router.websocket("/ws/market/{ticker}")
async def get_realtime_prices(websocket: WebSocket, ticker: str):
    await websocket.accept()
    stream = RealTimeMarketSerive()
    async for price in stream.subscribe("BINANCE:BTCUSDT"):
        await websocket.send_json({"price": price, "ticker": ticker})
