import websockets
import asyncio
from websockets.exceptions import ConnectionClosed, WebSocketException
import json
from stock_analysis.core.config import settings


class RealTimeMarketSerive:
    URL = "wss://ws.finnhub.io"

    def __init__(self) -> None:
        self.api_key = settings.finnhub_api_key

    async def subscribe(self, symbol: str):

        url = f"{self.URL}?token={self.api_key}"
        try:
            async with websockets.connect(url) as ws:
                print(f"connected to {url}")
                await ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

                print("subscribed to", symbol)

                while True:

                    try:
                        raw = await ws.recv()
                        data = json.loads(raw)
                        if data.get("type") == "trade" and "data" in data:
                            trade = data["data"][0]
                            price = trade["p"]
                            yield price

                        elif data.get("type") == "ping":
                            await ws.send(json.dumps({"type": "pong"}))
                            print("Ping received, Pong sent")
                    except ConnectionClosed as e:
                        print(f"Connection closed: {e}")
                        break
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse message: {e}")
                        continue

        except WebSocketException as e:
            print(f"WebSocket error: {e}")
        except Exception as e:
            print(f" Unexpected error: {e}")


# async def test():

#     stream = RealTimeMarketSerive()
#     await stream.subscribe("BINANCE:BTCUSDT")

# asyncio.run(test())
