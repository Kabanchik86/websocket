import asyncio, json, time, requests, websockets
from asyncio.exceptions import CancelledError


# WEBSOKET OKX#############################################

async def okx(prices):
    url = "wss://ws.okx.com:8443/ws/v5/public"
    INSTS = ["TON-USDT", "SUI-USDT", "APT-USDT", "NEAR-USDT", "ATOM-USDT", "AVAX-USDT", "DOT-USDT", "UNI-USDT", "PEPE-USDT",
             "RENDER-USDT", "TRUMP-USDT", "FIL-USDT", "FLR-USDT", "JUP-USDT", "PENGU-USDT"]
    while True:
        try:
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print("Connected_okx")
                # Сообщение для подписки
                subscribe_msg = {
                    "op": "subscribe",
                    "args": [{"channel": "books5", "instId": inst} for inst in INSTS]
                }
                await ws.send(json.dumps(subscribe_msg))
                async for msg in ws:
                    # Получаем пуши
                    inform = json.loads(msg)
                    # проверяем, что это стакан
                    if "data" not in inform or not inform["data"]:
                        continue

                    instId = inform["arg"]['instId']
                    data = inform["data"][0]
                    ask = float(data["asks"][0][0])
                    bid = float(data["bids"][0][0])
                    volume_ask = float(data["asks"][0][1])
                    volume_bid = float(data["bids"][0][1])

                    prices["okx"][instId] ={
                        "ask": ask,
                        "bid": bid,
                        "ask_qty": volume_ask,
                        "bid_qty": volume_bid,
                        "ts": int(data["ts"])  # OKX ts уже в мс строкой
                    }

        except CancelledError as e:
            print('Interrupted by user')
        except Exception as e:
            print(f"Reconnect after error: {type(e).__name__}: {e}")
            await asyncio.sleep(2)
